import streamlit as st
from api_service import *
from datetime import datetime
#config
st.set_page_config(page_title="Task manager pro",layout="wide")
#initialization
if "add_title" not in st.session_state:
    st.session_state.add_title=""
if "add_desc" not in st.session_state:
    st.session_state.add_desc=""
if "add_priority" not in st.session_state:
    st.session_state.add_priority="low"
if "add_due_date" not in st.session_state:
    st.session_state.add_due_date=datetime.today()
if "reset_form" not in st.session_state:
    st.session_state.reset_form=False

#reset fields after adding a task
if st.session_state.reset_form:
   st.session_state.add_title=""
   st.session_state.add_desc="" 
   st.session_state.add_priority='low'
   st.session_state.add_due_date=datetime.today()
   st.session_state.reset_form=False

#header
st.title("my task manager")

#add task
st.subheader("ADD TASK")
with st.form("add_task_form"):
    col1,col2=st.columns(2)
    with col1:
        title=st.text_input("title",key="add_title")
    with col2:
        discription =st.text_input("description",key="add_desc")
    priority=st.selectbox("priority",['low','medium','high'],key="add_priority")
    due_date=st.date_input("due date",key="add_due_date")
    submitted=st.form_submit_button("add task") 
    if submitted:
        if title.strip():
            add_task(title,discription,priority,str(due_date))   
            st.session_state.reset_form=True 
            st.success("task added")
            st.rerun()
        else:
            st.error("title is required")
st.divider()
#search box
search_query=st.text_input("search tasks",placeholder="type to search any task with its title....",key="search_input")

# fetch all tasks 
if search_query:
    tasks=search_tasks(search_query)
else:
    tasks=get_tasks()
st.divider()

# show task list 
st.subheader("your tasks")
if not tasks:
    st.info("no tasks found")
PRIORITY_LABELS= {
     "high":"high",
     "medium":"medium",
     "low":"low"
}
for task in tasks:
    with st.container():
        col1,col2,col3,col4=st.columns([5,2,2,1])
        with col1:
            st.markdown(f"**{task['title']}**")
            st.caption(task['description'])
        with col2:
            st.write(task["due_date"])
        with col3:
            st.markdown(f"**{PRIORITY_LABELS.get(task['priority'],task['priority'])}**")
        with col4:
            if st.button("edit",key=f"edit_{task['id']}"):
               st.session_state.edit_task=tasks
            if st.button("dalete",key=f"del_{task["id"]}"):
                delete_task(task["id"])
                st.sucess("task deleted")
                st.rerun()
            st.divider()
#edit task section
if "edit_task" in st.session_state:
    task=st.session_state.edit_task
    st.subheader("edit task")
    with st.form("edit_task_form"):
        new_title=st.text_input("title",value=task["title"],key='edit_title')
        new_desc=st.text_input("description",value=task["description"],key='edit_desc')
        new_priority=st.selectbox("priority",['low','medium','high'],index=["low",'medium','high'].index(task["priority"]),key='edit_priority') 
        default_date=datetime.strptime(task["due_date"],"%Y-%m-%d")
        new_date=st.date_input("due date",value=default_date,key="edit_due_Date")
        col1 ,col2=st.columns(2)
        with col1:
            save=st.form_submit_button("save changes")
        with col2:
            cancel=st.form_submit_button("cancel")
            if save:
                update_task(
                    task["id"],
                    new_title,
                    new_desc,
                    new_priority,
                    str(new_date),
                    task["completed"]
        
                )
                del st.session_state.edit_task
                st.success("task updated")
                st.rerun()
            if cancel:
                del st.session_state.edit_task
                st.rerun()





        
        

        


        
             

