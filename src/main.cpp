#include "XPEngine/XPEngine.hpp"

int main(int argc, const char* argv[]){
    XPE::Init();

    XPE::Window test_window = XPE::CreateWindow("Hello World!", 640, 360);
    XPE::Renderer test_renderer = XPE::CreateRenderer(&test_window);
    test_renderer.SetClearColour(1, 0, 0, 1);
    
    while(test_window.WindowShouldClose()){
        test_window.PollEvents();

        test_renderer.Clear();

        //do some rendering

        test_window.SwapBuffers();
    }

    test_window.Destroy();

    XPE::Quit();
    return 0;
}