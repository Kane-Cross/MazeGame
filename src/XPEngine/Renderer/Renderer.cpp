#include "Renderer.hpp"

namespace XPE{
    Renderer::Renderer(){}

    Renderer::Renderer(Window* window){
        parent_window = window;
    }

    bool Renderer::CreateRenderer(Window* window){
        parent_window = window;
        return true;
    }

    void Renderer::SetViewport(int x, int y, int width, int height){
        glViewport(x, y, width, height);
    }

    void Renderer::SetClearColour(float r, float g, float b, float a){
        glClearColor(r, g, b, a);
    }

    void Renderer::Clear(){
        glClear(GL_COLOR_BUFFER_BIT);
    }

    bool Renderer::IsValid(){
        return true;
    }

    void Renderer::Destroy(){
        
    }
}