import streamlit as st
from api import earley_parser
from NER_modules import markup_text
from io import StringIO
import base64
from PIL import Image


def find_matches(text, options):
    text = text.strip()
    if text:
        if any(options):
            results_list = []
            spans = []
            with st.spinner('Відбувається аналіз тексту...'):
                for index_option in range(len(options)):
                    if options[index_option]:
                        parsing_result = earley_parser(index_option, text)
                        results_list.append(parsing_result)

            st.success('Аналіз завершено!')
            for result in results_list:
                for match in result.matches:
                    res = str(match.fact).split(sep='(')
                    st.subheader(res[0])
                    st.write(match.fact.as_json)
                    spans.append([match.span[0], match.span[1], res[0]])
            st.write(markup_text(text, spans),unsafe_allow_html=True)

                    
        elif not any(options):
            st.error('Оберіть типи іменованих сутностей')
            
    elif not text:
        st.error('Введіть текст для аналізу')    

if __name__ == '__main__':

    #    .sidebar .sidebar-content {
    #         background: url("url_goes_here")
    #     }

    st.sidebar.title('Україномовний NER')

    user_choice = st.sidebar.radio('Сторінки системи', 
    ['Інструкція користувача', 'Добування фактів'])

    if user_choice == 'Інструкція користувача':
        background = "main_background.png"
        i0 = Image.open("00.png")
        i1 = Image.open("01.png")
        i2 = Image.open("02.png")
        i3 = Image.open("03.png")
        i4 = Image.open("04.png")
        welcome = Image.open("main_page.jpeg")
        
        st.markdown(
        f"""
        <style>
        .reportview-container {{
            background: url(data:image/{background};base64,{base64.b64encode(open(background, "rb").read()).decode()})
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
        st.title('Інформаційна система добування фактів з україномовних текстів')
        st.image(welcome, caption=' ', width=800, output_format='PNG')
        st.subheader("Система розроблена для вирішення задачі україномовного NER.")
        st.write("**Інструкція користувача для взаємодії з системою:**")
        st.write("➔ Після вибору сторінки добування фактів є вибір для введення тексту **[1] Власноруч** та **[2] Обравши файл**")
        st.image(i0, caption='Вибір введення тексту', output_format='PNG')
        st.write("➔ При виборі **[1]** з'являється **[1.1] поле для введення**")
        st.image(i1, caption='', output_format='PNG')
        st.write("➔ При виборі **[2]** з'являється відповідно **[1.1] завантажувач файлів**")
        st.image(i2, caption='', output_format='PNG')
        st.write("➔ За вибір типів фактів для добування відподівають **[3] чек-бокси**") 
        st.write("➔ Після надання вхідних даних для аналізу натискається кнопка **[4] запуск алгоритму**")
        st.write("➔ Процес аналізу тексту зображається за допомогою відповідного поля **[5]**")
        st.image(i3, caption='', output_format='PNG')
        st.write("➔ Користувача повідомляють про **[6] завершення аналізу** та надають звіт  **[7] добутих фактів**")
        st.image(i4, caption='', output_format='PNG')

        
        

    elif user_choice == 'Добування фактів':
        text = False
        st.title('Добування фактів з україномовних текстів')
        input_choice = st.selectbox('Оберіть тип введення тексту', 
                                    ['Вввести власноруч','Обрати файл'])
        if input_choice == 'Вввести власноруч':                            
            st.subheader('Введіть текст для аналізу')
            text = st.text_area(' ')
        elif input_choice == 'Обрати файл':
            uploaded_file = st.file_uploader(label="Завантажте локальний файл", type=['txt','doc','docx'])
            if uploaded_file:
                text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
                st.subheader("Текст з файлу")
                st.markdown("*{}*".format(text))   

        st.subheader('Типи іменованих сутностей для пошуку')
        cols = st.beta_columns(4)
        person_col = cols[0].checkbox("Персони (посада та ім'я)")
        name_col = cols[1].checkbox('Імена')
        location_col = cols[2].checkbox('Локація')
        date_col = cols[3].checkbox('Дати')
        options = [person_col, name_col, location_col, date_col]
        start = st.button('Запустити алгоритм добування фактів')
        
        if start and text: 
            find_matches(text, options)
        elif start and text != True:
            st.error('Введіть текст для аналізу')