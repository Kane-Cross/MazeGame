#include "XPEngine/XPEngine.hpp"

int main(int argc, const char* argv[]){
    XPE::Init();

    XPE::Window test_window = XPE::CreateWindow("Hello World!", 640, 360);

    

    XPE::Quit();
    return 0;
}