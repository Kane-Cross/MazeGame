#include "GLFWErrors.hpp"

#ifdef DEBUG
namespace XPE{
    void GLFWErrorCallback(int id, const char* description){}
}
#else
#include <iostream>
namespace XPE{
    void GLFWErrorCallback(int id, const char* description){
        std::cout << description << std::endl;
    }
}
#endif