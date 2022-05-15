import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_echarts import st_echarts
from PIL import Image
import seaborn as sns

img = Image.open("alco for project.jpg")
st.image(img, width=700)

def intro():
    st.header("Student Alcohol Consumption")
    st.subheader("Social, gender and study data from secondary school students")
    st.info("Анализ данных, полученных при опросе учащихся двух португальских школ. Датасет содержит информацию"
            "об успеваемости, семейном положении, возрасте и потреблении алкоголя учащимися.")
if __name__ == "__main__" :
    intro()

with st.echo(code_location='below'):
    @st.experimental_singleton()

    def get_file():
        return pd.read_csv('student-mat.csv')
    df=get_file()
    st.dataframe(df)
    print(df)

    meow = st.button("Алкоголь вредит моему здоровью!")
    meow
    if (meow):
        st.subheader("Пей водичку!!! :^)")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.subheader("Посмотрим на зависимость возраста и количества употребляемого алкоголя")
    df_age_alco=df.groupby('age', as_index=False).agg({'Walc':'mean', 'Dalc':'mean'})

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_age_alco['age'], y=df_age_alco['Walc'],  name='Weekend'))
    fig.add_trace(go.Bar(x=df_age_alco['age'], y=df_age_alco['Dalc'], name='Workday'))
    fig.update_layout(legend_title_text="Days", title="Потребление алкоголя в зависимости от возраста "
                                                      "(1-очень мало, 5-очень много)")
    fig.update_xaxes(title_text="Age")
    fig.update_yaxes(title_text="Alcohol consumption")
    st.plotly_chart(fig)
    st.write("По графику видно, что среди людей до 20 лет большая часть потребляемого "
             "алкоголя приходится на группу восемнадцатилетних. Это связано, в первоую очередь, "
             "с тем, что в это время многие португальские подростки выпускаются из "
             "школы и физически сепарируются от родителей. Так как в португалии нет возрастного "
             "ограничения на продажу и покупку алкоголя, потребление более юными подростками "
             "алкогольной продукции ненулевое.")


    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.subheader("Как влияет количество употребляемого в рабочие дни алкоголя на пропуски "
                 "занятий и время, которое ученики тратили на учёбу")
    df_alco_abs = df.groupby('Dalc', as_index=False).agg({'studytime': 'mean', 'absences': 'mean'})

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_alco_abs['Dalc'], y=df_alco_abs['absences'], name='Absences'))
    fig.add_trace(go.Bar(x=df_alco_abs['Dalc'], y=df_alco_abs['studytime'], name='Study time'))
    fig.update_layout(title="Время, потраченное на учёбу и пропуски занятий без уважительной причины")
    fig.update_xaxes(title_text="Workday alcohol consumption")
    fig.update_yaxes(title_text="Study time(hours)/Absences(days)")
    st.plotly_chart(fig)
    st.write("Как можно наблюдать, с ростом потребления алкоголя растет количество "
             "пропусков учебы без уважительной причины. Количество времени, "
             "потраченного на учебу, отрицательно зависит от количества потребляемого "
             "алкоголя в рабочие дни, однако ависимость выражена не очень ярко.")

    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.subheader("Как вы думаете, влияет ли количество употребляемого "
                         "алкоголя на оценку здоровья?")
    alco = st.radio("Влияет?",('Влияет', 'Не влияет'))
    if (alco=='Влияет'):
        st.error("Давайте посмотрим на данные")
    else:
        st.success("Верно, не влияет!")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.subheader("Как люди, употребляющие много алкоголя оцениваю свое здоровье")
    alco_health = df[["Walc","health"]]
    high_alco_health = alco_health[alco_health['Walc'] == 5]
    health = high_alco_health['health'].value_counts()
    soft_health = alco_health['health'].value_counts()

    health1 = str(health[1])
    health2 = str(health[2])
    health3 = str(health[3])
    health4 = str(health[4])
    health5 = str(health[5])

    soft_health1 = str(soft_health[1])
    soft_health2 = str(soft_health[2])
    soft_health3 = str(soft_health[3])
    soft_health4 = str(soft_health[4])
    soft_health5 = str(soft_health[5])


    options = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "1%", "left": "center"},
        "series": [
            {"name": "Оценка здоровья", "type": "pie", "radius": ["30%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {"borderRadius": 15,
            "borderColor": "#fff",
            "borderWidth": 3},
            "label": {"show": False, "position": "center"},
            "emphasis": {"label": {"show": True, "fontSize": "20", "fontWeight": "bold"}},
            "labelLine": {"show": False},
            "data": [{"value": health1, "name": "Очень плохо"},
                     {"value": health2, "name": "Плохо"},
                     {"value": health3, "name": "Удовлетворительно"},
                     {"value": health4, "name": "Хорошо"},
                     {"value": health5, "name": "Отлично"}]}]}

    st_echarts(options=options, height="600px")
    st.write("Как можно заметить по ответам респондентов, употребляющих наибольшее количество алкоголя, "
             "большое количество алкоголя, по их оценке не всегда ухудшает здоровье.")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.subheader("Для сравнения прведем такую же диаграму с данными по всем участникам опроса")
    options = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "1%", "left": "center"},
        "series": [
            {"name": "Оценка здоровья", "type": "pie", "radius": ["30%", "70%"],
             "avoidLabelOverlap": False,
             "itemStyle": {"borderRadius": 15,
                           "borderColor": "#fff",
                           "borderWidth": 3},
             "label": {"show": False, "position": "center"},
             "emphasis": {"label": {"show": True, "fontSize": "20", "fontWeight": "bold"}},
             "labelLine": {"show": False},
             "data": [{"value": soft_health1, "name": "Очень плохо"},
                      {"value": soft_health2, "name": "Плохо"},
                      {"value": soft_health3, "name": "Удовлетворительно"},
                      {"value": soft_health4, "name": "Хорошо"},
                      {"value": soft_health5, "name": "Отлично"}]}]}

    st_echarts(options=options, height="600px")
    st.markdown("Можно отметить, что люди, употребляющие больше алкоголя оценивают "
                "своё состояние здоровья в среднем лучше.")



    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.subheader("Посмотрим на влияние наличия романтических отношений на количество употребляемого "
                 "алкоголя")

    romantic = df[["romantic", "Walc"]]
    romantics = romantic['romantic'].value_counts()

    romantic_fig = sns.displot(x='Walc',
                hue='romantic',
                multiple='dodge',
                data=romantic)
    romantic_yes_no = sns.displot(x='romantic',
                               hue='romantic',
                               multiple='dodge',
                               data=romantic)

    st.pyplot(romantic_fig)
    if st.checkbox("Показать соотношение людей в отношениях и без"):
        st.pyplot(romantic_yes_no)
    st.write("Как можно заметить по графику, доля людей, употребляющих определенное количество "
             "алкоголя не меняется в зависимости от наличия или отсутствия отношений.")








