#include "XPEngine/XPEngine.hpp"

int main(int argc, const char* argv[]){
    XPE::Init();

    XPE::Window test_window = XPE::CreateWindow("Hello World!", 360, 640);

    test_window.Show();

    XPE::Breakpoint();

    XPE::Quit();
    return 0;
}