#include "XPEngine/XPEngine.hpp"

int main(int argc, const char* argv[]){
    XPE::Init();

    XPE::Window test_window = XPE::CreateWindow("Hello World!", 640, 360);
    
    while(test_window.WindowShouldClose()){
        test_window.PollEvents();

        //do some rendering

        test_window.SwapBuffers();
    }

    XPE::Quit();
    return 0;
}