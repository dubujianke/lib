
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

