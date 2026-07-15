import streamlit as st
import plotly.express as px
from Jobs_Mostaql import *
from Mostaql_data_refinement import *
import asyncio
import threading as th
import time
#session state
st.session_state.scraped_data = None
st.session_state.refined_data=None
st.session_state.url = None
st.session_state.desc = None
st.session_state.skills = None
st.session_state.badges = None
st.session_state.scraped_completed = False
st.session_state.orderType = True
st.session_state.c=None
st.session_state.d=None
st.session_state.disabled=False
st.session_state.search_term=None
st.session_state.erroring=False
st.session_state.cancel_e = th.Event()
st.session_state.cancell_ed=False
#fragmented and non-fragmented functions
@st.fragment
def scraping(search):
    def cancelled():
        st.session_state.cancel_e.set()
        st.session_state.scraped_data = None
        st.session_state.refined_data = None
        st.session_state.url = None
        st.session_state.desc = None
        st.session_state.skills = None
        st.session_state.badges = None
        st.session_state.scraped_completed = False
        st.session_state.orderType = True
        st.session_state.c = None
        st.session_state.d = None
        st.session_state.disabled = False
    def disable():
        st.session_state.disabled = True
    session = {}
    def scraping_op(cancel_operation,text):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            ex_data = loop.run_until_complete(mostaql_scrape(text,cancel_operation.is_set()))
            (ref_data,
             urls,
             desc_text,
             sk_sets,
             skill_badges) = data_refine(ex_data)
            opt_completed = True
            session['scraped'] = ex_data
            session['refined'] = ref_data
            session['urls'] = urls
            session['desc'] = desc_text
            session['skills'] = sk_sets
            session['badges'] = skill_badges
            session['completed'] = opt_completed
            return session
        except Exception:
            session['error'] = True
        finally:
            loop.close()
    scrape_button = st.button("SCRAPE", use_container_width=True,disabled=st.session_state.disabled,on_click=disable)
    thread = th.Thread(target=scraping_op, args=(st.session_state.cancel_e, search))
    st.session_state.cancel_e.clear()
    if scrape_button:
        st.button("CANCEL", width="stretch",on_click=cancelled)
        with st.spinner("Extracting Data..."):
            thread.start()
            thread.join()
            try:
                st.session_state.scraped_data = session['scraped']
                st.session_state.refined_data = session['refined']
                st.session_state.url = session['urls']
                st.session_state.desc = session['desc']
                st.session_state.skills = session['skills']
                st.session_state.badges = session['badges']
                st.session_state.scraped_completed = session['completed']
            except KeyError:
                st.session_state.erroring = session['error']
            if st.session_state.erroring:
                st.session_state.disabled = False
                st.error("Connection Refused , Please Try Again")
                time.sleep(5)
                st.rerun()
            elif st.session_state.scraped_completed:
                st.success("Extracting Completed!")
def main_sample(d_t,d_s):
    with d_t[d_s.index("Main")]:
        d0 = st.dataframe(data=st.session_state.refined_data.head(10), on_select="rerun", width="stretch",
                          selection_mode="single-row")
        desc_spc, skill_spc = st.columns([3, 1])
        if d0.selection.rows:
            row_num = d0.selection.rows[0]
            desc_spc.write(f"""
            ### Job Description:  \n
            {st.session_state.desc[row_num]}
                      """)
            with skill_spc.expander("Skills", expanded=False):
                st.markdown(st.session_state.badges[row_num])
            st.link_button("Go To", st.session_state.url[row_num], width="stretch")
def pay_sample(d_t,d_s):
    with d_t[d_s.index("Payment")]:
        term = st.selectbox(label="BY",
                            options=["Maximum Budget", "Minimum Budget", "Average Budget"])
        d1 = st.dataframe(data=st.session_state.refined_data.sort_Values(by=term,ascending=st.session_state.orderType).head(10),
                          on_select="rerun", width="stretch", selection_mode="single-row")
        desc_spc, skill_spc = st.columns([3, 1])
        if d1.selection.rows:
            row_num = d1.selection.rows[0]
            desc_spc.write(f"""
                                ### Job Description:  \n
                                {st.session_state.desc[row_num]}
                                          """)
            with skill_spc.expander("Skills", expanded=False):
                st.markdown(st.session_state.badges[row_num])
            st.link_button("Go To", st.session_state.url[row_num], width="stretch")
def accpt_sample(d_t,d_s):
    with d_t[d_s.index("Acceptance (%)")]:
        d2 = st.dataframe(data=st.session_state.refined_data.sort_values(by="Accepting Percentage",ascending=st.session_state.orderType).head(10),
                          on_select="rerun", width="stretch", selection_mode="single-row")
        desc_spc, skill_spc = st.columns([3, 1])
        if d2.selection.rows:
            row_num = d2.selection.rows[0]
            desc_spc.write(f"""
                                ### Job Description:  \n
                                {st.session_state.desc[row_num]}
                                          """)
            with skill_spc.expander("Skills", expanded=False):
                st.markdown(st.session_state.badges[row_num])
            st.link_button("Go To", st.session_state.url[row_num], width="stretch")
def recent_jobs(d_t,d_s):
    with d_t[d_s.index("Jobs Recency")]:
        d3 = st.dataframe(
            data=st.session_state.sort_values(by=["Posted Date", "Posted Time"],ascending=[st.session_state.orderType
                ,st.session_state.orderType]).refined_data.head(10),
            on_select="rerun", width="stretch", selection_mode="single-row")
        desc_spc, skill_spc = st.columns([3, 1])
        if d3.selection.rows:
            row_num = d3.selection.rows[0]
            desc_spc.write(f"""
                                ### Job Description:  \n
                                {st.session_state.desc[row_num]}
                                          """)
            with skill_spc.expander("Skills", expanded=False):
                st.markdown(st.session_state.badges[row_num])
            st.link_button("Go To", st.session_state.url[row_num], width="stretch")
def urgent_jobs(d_t,d_s):
    with d_t[d_s.index("Fin. Urgent")]:
        d4 = st.dataframe(
            data=st.session_state.refined_data.sort_values(by="Fin. Urgency",ascending=st.session_state.orderType).head(10),
            on_select="rerun", width="stretch", selection_mode="single-row")
        desc_spc, skill_spc = st.columns([3, 1])
        if d4.selection.rows:
            row_num = d4.selection.rows[0]
            desc_spc.write(f"""
                                ### Job Description:  \n
                                {st.session_state.desc[row_num]}
                                          """)
            with skill_spc.expander("Skills", expanded=False):
                st.markdown(st.session_state.badges[row_num])
            st.link_button("Go To", st.session_state.url[row_num], width="stretch")
def line_charts(c_t,c_s):
    with c_t[c_s.index("Line Charts")]:
        x1 = st.session_state.refined_data["Posted Date"].sort_values(ascending=st.session_state.orderType)
        y1 = st.session_state.refined_data["Posted Date"].value_counts().sort_values(
            ascending=st.session_state.orderType)
        line1 = px.line(x=x1, y=y1, title="AVG Number Of Jobs/Day", labels={'x': "TimeLine",
                                                                            'y': "No_Jobs"},
                        hover_data={'x': True, 'y': True}, template="plotly_dark", hover_name="Info")
        x2 = st.session_state.refined_data["Posted Time"].sort_values(ascending=st.session_state.orderType)
        y2 = st.session_state.refined_data["Posted Time"].value_counts().sort_values(
            ascending=st.session_state.orderType)
        line2 = px.line(x=x2, y=y2, title="AVG Number Of Jobs/Hour", labels={'x': "TimeLine",
                                                                             'y': "No_Jobs"},
                        hover_data={'x': True, 'y': True}, hover_name="Info", template="plotly_dark")
        st.plotly_chart(line1, use_container_width=True, theme="streamlit")
        st.plotly_chart(line2, use_container_width=True, theme="streamlit")
def bar_charts(c_t,c_s):
    with c_t[c_s.index("Bar Charts")]:
        bar_samp = st.session_state.refined_data
        bar1 = px.bar(
            data_frame=bar_samp.sort_values(by="Fin. Urgency", ascending=st.session_state.orderType, inplace=True),
            x="Title", y="Fin. Urgency", labels={'x': "Title",
                                                 'y': "Financial Urgency"}, title="Fin. Urgent Jobs",
            color='#32a84e', template="plotly_dark",
            hover_name="Title", hover_data={
                "Average Budget": True,
                "Time Interval (Days)": True,
                "Fin. Urgency": True
            })
        temp0 = st.session_state.skills.merge(st.session_state.refined_data[["Average Budget", "Time Interval (Days)"]],
                                              left_index=True, right_index=True)
        skills = temp0["Skill Sets"].explode()
        count = skills.values_count()
        grouped_skills = temp0.groupby("Skill Sets")[["Average Budget", "Time Interval (Days)"]].mean()
        skills_data = pd.DataFrame(
            {"skills": skills.drop_dubplicates(inplace=True, ignore_index=True), "count": count}).sort_values(
            by="count", ascending=st.session_state.orderType)
        bar2 = px.bar(skills_data, x="skills", y="count", title="Skills Frequency", template="plotly_dark",
                      labels={'x': "Skills", 'y': "Frequency"}, hover_name="Info"
                      , hover_data={
                "Average Payment": grouped_skills["Average Budget"],
                "Average DeadLine": grouped_skills["Time Interval (Days)"]
            }, color="#2936cc")
        st.plotly_chart(bar1, use_container_width=True, theme="streamlit")
        st.plotly_chart(bar2, use_container_width=True, theme="streamlit")
def heatmaps(c_t,c_s):
    with c_t[c_s.index("Heat Maps")]:
        # first map
        temp1 = st.session_state.skills.merge(st.session_state.refined_data["Number of Proposals"], left_index=True,
                                              right_index=True)
        temp1["Skill Sets"] = temp1["Skill Sets"].explode()
        frq_skills = temp1.groupby("Skill Sets")["Number of Proposals"].median().unstack()
        hm1 = px.imshow(frq_skills, text_auto='.0f', aspect="auto", color_continuous_scale="RdBu",
                        title="Most Frequent Skills")
        st.plotly_chart(hm1, use_container_width=True, theme="streamlit")
        # second map
        corr = st.session_state.refined_data[["Number of Proposals", "Time Interval (Days)"]].corr()
        hm2 = px.imshow(corr, text_auto='.0f', aspect="auto", color_continuous_scale="RdBu", zmin=-1, zmax=1,
                        title="Correlations Of Jobs Info")
        st.plotly_chart(hm2, use_container_width=True, theme="streamlit")
#title
st.markdown("<h1 style='text-align: center;'>Mostaql Data Extraction</h1>", unsafe_allow_html=True)
#setting Sidebar tabs
st.sidebar.title("Filtering Panel")
with st.sidebar.form(key="filter-form-1"):
    charts = st.expander("Analytics Dashboard")
    s_data = st.expander("Data Sample")
    st.session_state.c = charts.multiselect(options=["Line Charts", "Bar Charts", "Heat Maps"], label="Charts Filter")
    st.session_state.d = s_data.multiselect(
        options=["Main", "Payment", "Acceptance (%)", "Jobs Recency", "Fin. Urgent"], label="Data Filter")
    order = st.selectbox("Order", ["Ascending", "Descending"])
    if order == "Descending":
        st.session_state.orderType = False
    else:
        st.session_state.orderType = True
    if st.form_submit_button("Apply Filters",width="stretch"):
        st.success("Filters applied")
#setting upper topic layouts
cont=st.container(horizontal=True)
cont.write("""
        ### Message 
        ##### This is a training app on the fundamentals of **Streamlit**
        ###### by doing a mock project of a *web scraping website* that scrapes a freelance website and analyse its data. 
        ###### To see more of those projects follow-up on my GitHub : https://github.com/ahmedkhalid6634-creator/my_projects.git
        """)
with st.expander("Used Frameworks",expanded=False):
    st.write("""
        ##### 1 - Python 🐍
        ##### 2 - Streamlit ⛵
        ##### 3 - Pandas 🐼
        ##### 4- PlayWright 🎭
        ##### 5 - Plotly 📊
            """)
cont2=st.container(horizontal=True)
cont2.info("**NOTE** : typing in the search bar is **OPTIONAL**")
st.divider()
#scraping session starts HERE !!
sp1,c,sp2=st.columns([2,4,1])
c.write("#### To start extracting Press **EXTRACT**")
st.session_state.search_term=st.text_input("**Search**")
scraping(search=st.session_state.search_term)
st.divider()
#Data Analyzed HERE !!
if st.session_state.scraped_completed:
    cols = st.columns(2)
    data_samp = cols[0].container(horizontal=True, horizontal_alignment="left")
    draws = cols[1].container(horizontal=True, horizontal_alignment="right")
    with data_samp:
        data_but = st.button("**Scraped Data Sample**")
    with draws:
        dash_but = st.button("**Data Analytics Dashboard**")
    main = st.container(vertical_alignment="center")
    d_select = st.session_state.d
    c_select = st.session_state.c
    with main:
        space1,head,ordering=st.columns([3.1,4,1.7])
        if data_but:
            head.header("Data Samples")
            try:
                d_tabs = st.tabs(d_select)
            except Exception:
                pass
            if "Main" in d_select:
                main_sample(d_tabs,d_select)
            elif "Payment" in d_select:
                pay_sample(d_tabs,d_select)
            elif "Acceptance (%)" in d_select:
                accpt_sample(d_tabs,d_select)
            elif "Jobs Recency" in d_select:
                recent_jobs(d_tabs,d_select)
            elif "Fin. Urgent" in d_select:
                urgent_jobs(d_tabs,d_select)
        if dash_but:
            head.header("Data Charts")
            try:
                c_tabs = st.tabs(c_select)
            except Exception:
                pass
            if "Line Charts" in c_select:
                line_charts(c_tabs,c_select)
            if "Bar Charts" in c_select:
                bar_charts(c_tabs,c_select)
            if "Heat Maps" in c_select:
                heatmaps(c_tabs,c_select)