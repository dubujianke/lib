#ifdef WIN32
#include "net/MKUDPSocket.h"
#include "curl/curl.h"
#include <string>
#include <iostream>
#include <vector>
#include <tuple>
#include <cstdint>
#include <cstring>
#include <stdexcept>
#include <type_traits>
#include <sstream>  
#include "ESContext.h"
#define BUF_SIZE 1024
using namespace std;

// 字节序转换：Windows 兼容版本
inline uint16_t swap16(uint16_t val) {
    return (val << 8) | (val >> 8);
}

inline uint32_t swap32(uint32_t val) {
    return (val << 24) |
        ((val << 8) & 0x00FF0000) |
        ((val >> 8) & 0x0000FF00) |
        (val >> 24);
}

inline uint64_t swap64(uint64_t val) {
    return ((val & 0x00000000000000FFULL) << 56) |
        ((val & 0x000000000000FF00ULL) << 40) |
        ((val & 0x0000000000FF0000ULL) << 24) |
        ((val & 0x00000000FF000000ULL) << 8) |
        ((val & 0x000000FF00000000ULL) >> 8) |
        ((val & 0x0000FF0000000000ULL) >> 24) |
        ((val & 0x00FF000000000000ULL) >> 40) |
        ((val & 0xFF00000000000000ULL) >> 56);
}

template <typename T>
T from_bytes(const uint8_t* data, bool big_endian) {
    T value;
    std::memcpy(&value, data, sizeof(T));

    if (big_endian) {
        if (sizeof(T) == 2)
            value = static_cast<T>(swap16(*reinterpret_cast<uint16_t*>(&value)));
        else if (sizeof(T) == 4) {
            uint32_t v = swap32(*reinterpret_cast<uint32_t*>(&value));
            char* v2 = (char*)&v;
            value = *(T*)(v2);
        }
        else if (sizeof(T) == 8)
            value = static_cast<T>(swap64(*reinterpret_cast<uint64_t*>(&value)));
    }
    return value;
}

// 类型映射
template<char C> struct FormatMap;

template<> struct FormatMap<'b'> { using type = int8_t; };
template<> struct FormatMap<'B'> { using type = uint8_t; };
template<> struct FormatMap<'h'> { using type = int16_t; };
template<> struct FormatMap<'H'> { using type = uint16_t; };
template<> struct FormatMap<'i'> { using type = int32_t; };
template<> struct FormatMap<'I'> { using type = uint32_t; };
template<> struct FormatMap<'f'> { using type = float; };
template<> struct FormatMap<'d'> { using type = double; };

// 解包实现
template<std::size_t Index = 0, typename... Types>
typename std::enable_if<Index == sizeof...(Types), void>::type
unpack_tuple(const std::string& format, const std::vector<uint8_t>& buffer, std::tuple<Types...>& result, std::size_t& offset, bool big_endian) {
    // 完成递归
}

template<std::size_t Index = 0, typename... Types>
typename std::enable_if < Index < sizeof...(Types), void>::type unpack_tuple(const std::string& format, const std::vector<uint8_t>& buffer,
        std::tuple<Types...>& result, std::size_t& offset, bool big_endian) {

    typedef typename std::tuple_element<Index, std::tuple<Types...>>::type T;
    if (offset + sizeof(T) > buffer.size())
        throw std::runtime_error("Buffer too small");

    T value = from_bytes<T>(&buffer[offset], big_endian);
    std::get<Index>(result) = value;
    offset += sizeof(T);

    unpack_tuple<Index + 1>(format, buffer, result, offset, big_endian);
}

template<char... Chars>
std::tuple<typename FormatMap<Chars>::type...> unpack(const std::string& format, const std::vector<uint8_t>& buffer) {
    constexpr std::size_t N = sizeof...(Chars);
    typedef std::tuple<typename FormatMap<Chars>::type...> ResultTuple;
    ResultTuple result;

    std::size_t offset = 0;
    bool big_endian = false;

    std::string fmt = format;
    if (!fmt.empty() && fmt[0] == '!') {
        big_endian = true;
        fmt = fmt.substr(1);
    }

    if (fmt.size() != N)
        throw std::runtime_error("Format string does not match template parameters");

    unpack_tuple(fmt, buffer, result, offset, big_endian);
    return result;
}

class CBuffer {

public:
    char* buf;
    int total;
    bool isBig = false;
    CBuffer(char* buf, int total, bool isBig) {
        this->buf = buf;
        this->total = total;
        this->isBig = isBig;
    }
    int getInt(char* buf) {
        char* tmp = buf;
        char v[4] = {0};
        for (int i = 0; i < 4; i++) {
            if (isBig) {
                v[i] = tmp[4-1-i];
            }
            else {
                v[i] = tmp[i];
            }
        }
        int ret = *(int*)v;
        return ret;
    }
    int getShort(char* buf) {
        char* tmp = buf;
        char v[2] = { 0 };
        int len = 2;
        for (int i = 0; i < len; i++) {
            if (isBig) {
                v[i] = tmp[len - 1 - i];
            }
            else {
                v[i] = tmp[i];
            }
        }
        short ret = *(short*)v;
        return ret;
    }
    char* getSub(char* buf, int from, int end) {
        int v = 0;
        char* tmp = new char[end-from];
        for (int i = 0; i < end - from; i++) {
            tmp[i] = buf[from+i];
        }
        return tmp;
    }

    std::vector<uint8> copyMsg(char* message, int from, int end) {
        std::vector<uint8> message2;
        char* ret = getSub(message, from, end);
        message2.insert(message2.begin(), ret, ret+(end-from));
        return message2;
    }

    int getSubShort(char* buf, int from, int end) {
        short v = 0;
        char* tmp = new char[end - from];
        for (int i = 0; i < end - from; i++) {
            tmp[i] = buf[from + i];
        }
        v = getInt(tmp);
        delete tmp;
        return v;
    }

};


MKUDPSocket::MKUDPSocket(void)
{
	timeout = 30;
}

MKUDPSocket::~MKUDPSocket(void)
{

}

MKUDPSocket* MKUDPSocket::getInstance() {
    MKUDPSocket pMKUDPSocket;
    return &pMKUDPSocket;
}
void  MKUDPSocket::start() {
    run();
   /* thread_ = std::thread([this]() {
        run();
    });
    thread_.detach();*/
}

string getN(char c, int n) {
    stringstream ostr("");
    ostr.put('!');
    for (int i = 0; i < n; i++) {
        ostr.put(c);
    }
    string gstr = ostr.str();
    return gstr;
}

int MKUDPSocket::run() {

    WORD wVersionRequested;
    WSADATA wsaData = { 0 };
    wVersionRequested = MAKEWORD(2, 2);
    if (WSAStartup(wVersionRequested, &wsaData) != 0)
    {
        return 1;
    }
    if (LOBYTE(wsaData.wVersion) != 2 ||
        HIBYTE(wsaData.wVersion) != 2)
    {
        WSACleanup();
        return 1;
    }
    int nResult = 0;
    SOCKET ListenSocket = socket(AF_INET, SOCK_DGRAM, 0);
    if (INVALID_SOCKET == ListenSocket)
    {
        printf("create socket error (%d)\n", ::WSAGetLastError());
        WSACleanup();
        return 1;
    }
    SOCKADDR_IN addrSrv;
    memset(&addrSrv, 0, sizeof(addrSrv));
    addrSrv.sin_family = AF_INET;
    addrSrv.sin_port = htons(6000);
    addrSrv.sin_addr.s_addr = inet_addr("192.168.0.103");
    nResult = bind(ListenSocket, (SOCKADDR*)&addrSrv, sizeof(SOCKADDR_IN));
    char message[BUF_SIZE];
    std::vector<uint8> message2;
    message2.resize(BUF_SIZE);
    struct sockaddr_in clntAddr;
    int szClntAddr = sizeof(clntAddr);
    if (nResult == SOCKET_ERROR)
    {
        printf("bind socket error code = %d\n", ::WSAGetLastError());
        closesocket(ListenSocket);
        WSACleanup();
        return 1;
    }
    printf("服务端启动监听...\n");
    while (TRUE)
    {
        memset(message, 0, BUF_SIZE);        
        int strLen = recvfrom(ListenSocket, message, BUF_SIZE, 0, (struct sockaddr*)&clntAddr, &szClntAddr);
        if (strLen == SOCKET_ERROR) {
            std::cerr << "recvfrom failed: " << WSAGetLastError() << std::endl;
            break;
        }
        if (strLen>0) {
            message2.insert(message2.begin(), message, message + sizeof(message) / sizeof(message[0]));
            printf("-------------------------------> %d\n", strLen);
            CBuffer buffer(message, strLen, true);
            int name_length = buffer.getInt(buffer.getSub(message, 41, 45));
            int name_end_pos = 45 + name_length;
            if (strLen > name_end_pos + 16) {
                auto result = unpack<'i', 'f', 'i', 'i', 'b'>("!if2ib", buffer.copyMsg(message, name_end_pos, name_end_pos +17));
                int32_t _frame_number = std::get<0>(result);
                float _sub_frame = std::get<1>(result);
                int32_t _fps = std::get<2>(result);
                int32_t _denominator = std::get<3>(result);
                int8_t v = std::get<4>(result);
                for (int j = 0; j < 52; j++) {
                    auto ret = unpack<'f'>("!f", buffer.copyMsg(message, name_end_pos+17+j*4, name_end_pos + 17+j*4+4));
                    float item = std::get<0>(ret);
                    printf("/W %d %.5f\n", j, item);
                }
            }
        }
        //sendto(ListenSocket, message, strLen, 0, (struct sockaddr*)&clntAddr, sizeof(clntAddr));
    }

    closesocket(ListenSocket);
    WSACleanup();
    return 0;
}
#endif