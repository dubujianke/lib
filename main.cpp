#include <iostream>
#include <algorithm>
#include <memory>
#include <vector>
#include <exception>
#include <string>

#include <v8.h>
#include <libplatform/libplatform.h>

#include "v8pp/context.hpp"
#include "v8pp/version.hpp"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "v8.h"
#include <v8pp/call_v8.hpp>
#include <v8pp/function.hpp>
#include <v8pp/object.hpp>
#include <v8pp/class.hpp>
#include <v8pp/module.hpp>
#include "test.hpp"

using namespace v8;

namespace gbf {
namespace math {

static int yy(int a);
class Vector3
{
public:
	double x;
	double y;
	double z;

	Vector3()
		: x(0.0), y(0.0), z(0.0) {}
	Vector3(double _x, double _y, double _z)
		: x(_x), y(_y), z(_z) {
	}

	~Vector3() {
	}

	int var = 9;
	int get() const { return var; }
	void set(int v) { 
		var = v;
	}
	// Returns the length (magnitude) of the vector.
	double Length() {
		return 0;
	}

	int test(Vector3& x) {
		//x.x += 10;
		return x.x + x.y; 
	}

	/// Extract the primary (dominant) axis from this direction vector
	//const Vector3& PrimaryAxis() const;
};

}
} // namespace gbf::math

static int yy(int a)
{
	return a;
}

void test_class();
void ff(v8pp::context& context)
{
	v8::Isolate* isolate = context.isolate();
	v8::HandleScope scope(isolate);
	v8pp::class_<gbf::math::Vector3> math_vector3_class(isolate);
	math_vector3_class
		.ctor<double, double, double>()
		.var("var", &gbf::math::Vector3::var)
		.function("Length", &gbf::math::Vector3::Length)
		.function("test", &gbf::math::Vector3::test)
		.var("x", &gbf::math::Vector3::x)
		.var("y", &gbf::math::Vector3::y)
		.var("z", &gbf::math::Vector3::z)
		.property("wprop", &gbf::math::Vector3::get, &gbf::math::Vector3::set)
		.auto_wrap_objects(true);
	v8pp::module math_module(isolate);
	math_module.class_("Vector3", math_vector3_class);
	context.module("math3d", math_module);
	context.function("yfun", yy);

}


int main(int argc, char const* argv[])
{
	std::vector<std::string> scripts;
	std::string lib_path;
	bool do_tests = false;

	scripts.push_back("D:\\study\\v8pp-master\\1.js");
	// allow Isolate::RequestGarbageCollectionForTesting() before Initialize()
	// for v8pp::class_ tests
	//v8::V8::SetFlagsFromString("--expose_gc");
	//v8::V8::InitializeICU();
	v8::V8::InitializeExternalStartupData(argv[0]);
#if V8_MAJOR_VERSION >= 7
	std::unique_ptr<v8::Platform> platform(v8::platform::NewDefaultPlatform());
#else
	std::unique_ptr<v8::Platform> platform(v8::platform::CreateDefaultPlatform());
#endif
	v8::V8::InitializePlatform(platform.get());
	v8::V8::Initialize();
	//test_class();
	//test_call_from_v81();
	int result = EXIT_SUCCESS;
	try
	{
		v8pp::context context;
		ff(context);
		if (!lib_path.empty())
		{
			context.set_lib_path(lib_path);
		}
		for (std::string const& script : scripts)
		{
			v8::HandleScope scope(context.isolate());
			v8::Local<v8::Value> result = context.run_file(script);
			int m = v8pp::from_v8<int>(context.isolate(), result);
		}
		//int a = run_script<int>(context, "x = new math3d.Vector3(1,1,1); x.x += 10;");
	}
	catch (std::exception const& ex)
	{
		std::cerr << ex.what() << std::endl;
		result = EXIT_FAILURE;
	}

	v8::V8::Dispose();
#if V8_MAJOR_VERSION > 9 || (V8_MAJOR_VERSION == 9 && V8_MINOR_VERSION >= 8)
	v8::V8::DisposePlatform();
#else
	v8::V8::ShutdownPlatform();
#endif

	return result;
}
