#include "Renderer.hpp"

namespace XPE{
    Renderer::Renderer(){}

    Renderer::Renderer(Window* window){
        parent_window = window;
    }

    bool Renderer::CreateRenderer(Window* window){
        parent_window = window;
    }

    void Renderer::SetViewport(int x, int y, int width, int height){
        glViewport(x, y, width, height);
    }

    bool Renderer::IsValid(){
        
    }

    void Renderer::Destroy(){
        
    }
}