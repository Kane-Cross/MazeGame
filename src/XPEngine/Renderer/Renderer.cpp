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

    void Renderer::Clear(){
        glClearColor(0.0f, 0.5f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);
    }

    bool Renderer::IsValid(){
        
    }

    void Renderer::Destroy(){
        
    }
}