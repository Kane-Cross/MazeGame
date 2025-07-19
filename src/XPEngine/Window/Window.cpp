#include "Window.hpp"

namespace XPE{
    void Window::WindowResizeCallback(GLFWwindow* window, int width, int height){
        Window* resized_window = reinterpret_cast<Window*>(glfwGetWindowUserPointer(window));
        resized_window->SetViewport(0, 0, width, height);
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

    void Window::Resize(int width, int height){
        glfwSetWindowSize(window, width, height);
    }

    void Window::GetSize(int* w, int* h){
        glfwGetFramebufferSize(window, w, h);
    }

    void Window::SwapBuffers(){
        glfwSwapBuffers(window);
    }

    void Window::PollEvents(){
        glfwPollEvents();
    }

    bool Window::WindowShouldClose(){
        return glfwWindowShouldClose(window) == 0;
    }

    bool Window::IsValid(){
        return window == nullptr;
    };

    void Window::Destroy(){
        glfwDestroyWindow(window);
    }
}