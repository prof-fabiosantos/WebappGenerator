import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import PIL.Image
import time

from plantuml import PlantUML 
# Cria uma instância do PlantUML
plantuml = PlantUML("http://www.plantuml.com/plantuml/img/")

# Configurar a chave da API
genai.configure(api_key="AIzaSyAt0u96OqVw5-rAdM3pmL1rjT8H_jYAnJ8")

def remover_acentos_graves(s):
    # Substitui "```" por uma string vazia
    s = s.replace("```", "")
    s = s.replace("plantuml", "")
    
    return s


def generate_webapp():
    # Título do aplicativo Streamlit
    st.title("Generative AI Web Apps")
    st.subheader("Gera código a partir do Diagrama de Casos de Uso:")
    # Área de upload de imagem
    uploaded_file = st.file_uploader("Escolha um diagrama de casos de uso", type=["jpg", "jpeg", "png"])

    # Caixa de seleção para permitir que o usuário forneça um prompt personalizado
    use_custom_prompt = st.checkbox("Clique aqui se deseja fornecer um prompt personalizado")

    if use_custom_prompt:
        # Caixa de texto para o prompt personalizado (aparece apenas se use_custom_prompt for True)
        user_prompt = st.text_area("Digite seu prompt para gerar o código da app:", key="custom_prompt", value="")

    # Verificar se uma imagem foi carregada
    if uploaded_file is not None:
        # Carregar a imagem usando PIL
        img = PIL.Image.open(uploaded_file)
        # Exibir a imagem no frontend
        st.image(img, caption="Imagem Carregada", use_column_width=True)
        
        with st.spinner("Processando imagem..."):
            vision_description = None
            # Gerar descrição da imagem usando gemini-pro-vision
            model_vision = genai.GenerativeModel('gemini-pro-vision')
            vision_description = model_vision.generate_content(["Descreve com detalhes o que vê neste diagrama de casos de uso, especifique cada caso e ator mostrado no diagrama da imagem ", img])

            # Exibir a descrição no frontend
            st.subheader("Descrição do diagrama:")
            st.write(vision_description.text)
        
        with st.spinner("Gerando o código da app..."):
            # Usar o prompt personalizado fornecido pelo usuário se a opção estiver ativada
            if use_custom_prompt and user_prompt:
                prompt_text = user_prompt + ","+vision_description.text
            else:
                # Caso contrário, use o prompt padrão combinado com a descrição da imagem
                prompt_text = "Você é um desenvolvedor de web apps. Escreva os códigos necessários (não coloque nenhum comentário, somente os códigos) usando programação orientada a objetos, Python, Streamlit e caso seja necessário o banco de dados e suas tabelas usando o SQLite visando desenvolver um web app de acordo com a descrição deste diagrama de casos : " + vision_description.text
                
            # Gerar código usando o modelo gemini-pro
            model_code = genai.GenerativeModel('gemini-pro')
            generated_code = model_code.generate_content(prompt_text)

            # Exibir o código gerado no frontend
            st.subheader("Código Gerado:")
            st.code(generated_code.text, language='python')

            prompt_UML = "Escreva somente o código do script usando plantuml para geração do digrama de classes tendo como base o seguinte código:"+generated_code.text
            # Gerar código usando o modelo gemini-pro
            model_code = genai.GenerativeModel('gemini-pro')
            generated_code = model_code.generate_content(prompt_UML)         
           
            resultado = remover_acentos_graves(generated_code.text)

            print(resultado)
            with st.spinner("Gerando o diagrama de classes da app..."):
                # Gera o diagrama e salva como um arquivo PNG
                image_path = plantuml.processes(resultado)
                with open("class_diagram.png", "wb") as f:
                    f.write(image_path)
                
                time.sleep(5)
                st.subheader("Diagrama de Classes Gerado:")
                st.image("class_diagram.png") 

def reverse_engineering():
    # Título do aplicativo Streamlit
    st.title("Reverse Engineering Web Apps")
    st.subheader("Gera código a partir do Diagrama de Classes:")
    # Área de upload de imagem
    uploaded_file = st.file_uploader("Escolha um diagrama de classes", type=["jpg", "jpeg", "png"])

    # Caixa de seleção para permitir que o usuário forneça um prompt personalizado
    use_custom_prompt = st.checkbox("Clique aqui se deseja fornecer um prompt personalizado")

    if use_custom_prompt:
        # Caixa de texto para o prompt personalizado (aparece apenas se use_custom_prompt for True)
        user_prompt = st.text_area("Digite seu prompt para gerar o código da app:", key="custom_prompt", value="")

    # Verificar se uma imagem foi carregada
    if uploaded_file is not None:
        # Carregar a imagem usando PIL
        img = PIL.Image.open(uploaded_file)
        # Exibir a imagem no frontend
        st.image(img, caption="Imagem Carregada", use_column_width=True)
        
        with st.spinner("Processando imagem..."):
            vision_description = None
            # Gerar descrição da imagem usando gemini-pro-vision
            model_vision = genai.GenerativeModel('gemini-pro-vision')
            vision_description = model_vision.generate_content(["Descreve com detalhes o que vê neste diagrama de casos de classes, especifique cada classs e seus métodos mostrados no diagrama da imagem ", img])

            # Exibir a descrição no frontend
            st.subheader("Descrição do diagrama:")
            st.write(vision_description.text)
        
        with st.spinner("Gerando o código da app..."):
            # Usar o prompt personalizado fornecido pelo usuário se a opção estiver ativada
            if use_custom_prompt and user_prompt:
                prompt_text = user_prompt + ","+vision_description.text
            else:
                # Caso contrário, use o prompt padrão combinado com a descrição da imagem
                prompt_text = "Você é um desenvolvedor de web apps. Escreva os códigos necessários (não coloque nenhum comentário, somente os códigos) usando programação orientada a objetos, Python, Streamlit e caso seja necessário o banco de dados e suas tabelas usando o SQLite visando desenvolver um web app de acordo com a descrição deste diagrama de casos : " + vision_description.text
                
                          
            # Gerar código usando o modelo gemini-pro
            model_code = genai.GenerativeModel('gemini-pro')
            generated_code = model_code.generate_content(prompt_text)

            # Exibir o código gerado no frontend
            st.subheader("Código Gerado:")
            st.code(generated_code.text, language='python')
          
 
def main():
    st.sidebar.title("Menu")
    menu_option = st.sidebar.radio("Escolha uma opção", ["Generate Webapp", "Reverse Engineering"])

    if menu_option == "Generate Webapp":
        generate_webapp()
    elif menu_option == "Reverse Engineering":
        reverse_engineering()


if __name__ == "__main__":
    main()


   
       

           

       
        


            
            


                
            

