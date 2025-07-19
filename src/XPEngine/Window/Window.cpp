#include "Window.hpp"

namespace XPE{
    static void XPEWindowResizeCallback(GLFWwindow* window, int width, int height){
        
    }

    Window::Window(){};

    Window::Window(const char* title, int width, int height){
        CreateWindow(title, width, height);
    };

    bool Window::CreateWindow(const char* title, int width, int height){
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 6);
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
        window = glfwCreateWindow(width, height, title, nullptr, nullptr);
        glfwMakeContextCurrent(window);
        if(!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)){
            error = true;
            return false;
        }
        glViewport(0, 0, width, height);
        glfwSetWindowUserPointer(window, this);
        glfwSetFramebufferSizeCallback(window, WindowResizeCallback);
        error = !IsValid();
        return error;
    };

    void Window::Show(){
        glfwShowWindow(window);
    }

    void Window::Hide(){
        glfwHideWindow(window);
    }

    bool Window::IsValid(){
        return window == nullptr;
    };

    Window::~Window(){
        if(window != nullptr){
            glfwDestroyWindow(window);
        }
    }
}