from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts= [
    {
        "id": 1,
        "titulo": "Meu primeiro post",
        "resumo": "Resumo...",
        "conteudo": "Conteúdo completo...",
        "autor": "Carlos"
    }
]


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"posts": posts}
    )

@app.get("/post/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: int):

    post_encontrado = None

    for post in posts:
        if int(post["id"]) == id:
            post_encontrado = post
            break

    return templates.TemplateResponse(
        request=request,
        name="index.html",
       context={"post": [post_encontrado]}
    )

@app.get("/create", response_class=HTMLResponse)
async def create_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="criar_post.html"
    )

@app.post("/create")
async def create_post(request: Request):
    form = await request.form()
    novo_post = {
        "id":form.get("id"),
        "titulo": form.get("titulo"),
        "resumo": form.get("resumo"),
        "conteudo": form.get("conteudo"),
        "autor": form.get("autor")
    }

   
    posts.append(novo_post)

    return RedirectResponse(url="/", status_code=303)


@app.get("/edit/{id}", response_class=HTMLResponse)
async def create_page(request: Request, id:int):
    post_encontrado = None

    for post in posts:
        if int(post["id"]) == id:
            post_encontrado = post
            break

    return templates.TemplateResponse(
        request=request,
        name="editar_post.html",
       context={"post": [post_encontrado]}
    )

@app.post("/edit/{id}")
async def edit_post(request: Request, id: int):
    form = await request.form()

    for post in posts:
        if int(post["id"]) == id:
            post["id"] = id
            post["titulo"] = form.get("titulo")
            post["resumo"] = form.get("resumo")
            post["conteudo"] = form.get("conteudo")
            post["autor"] = form.get("autor")
            break

    return RedirectResponse(url="/", status_code=303)
    
@app.post("/delete/{id}")
async def delete_post(request: Request, id: int):

    for post in posts:
        if int(post["id"]) == id:
            posts.pop(posts.index(post))
            break

    return RedirectResponse(url="/", status_code=303)