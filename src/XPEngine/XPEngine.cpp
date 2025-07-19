#include "XPEngine.hpp"

#include <vector>
#include <iostream>

namespace XPE{
    bool Init(){
        int result = glfwInit();
        glfwSetErrorCallback(GLFWErrorCallback);
        return result == GLFW_TRUE;
    }

    void Quit(){
        glfwTerminate();
    }
}