#include "XPEngine.hpp"

namespace XPE{
    bool Init(){
        return glfwInit() == GLFW_TRUE;
    }

    void Quit(){
        glfwTerminate();
    }
}