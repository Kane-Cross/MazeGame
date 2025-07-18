#include "Window.hpp"

namespace XPE{
    Window::Window(){};

    Window::Window(const char* title, int width, int height){
        CreateWindow(title, width, height);
    };

    bool Window::CreateWindow(const char* title, int width, int height){
        
        return IsValid();
    };

    bool Window::IsValid(){
        return window == nullptr;
    };

    Window::~Window(){
        glfwDestroyWindow(window);
    }
}