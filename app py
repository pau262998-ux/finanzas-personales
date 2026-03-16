import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Mi dashboard financiero")

archivo = st.file_uploader("Sube tu archivo de Budge")

if archivo:

    if archivo.name.endswith(".csv"):
        df = pd.read_csv(archivo,encoding="latin1",skiprows=4)
    else:
        df = pd.read_excel(archivo)

    df["Amount"] = pd.to_numeric(df["Amount"],errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"],dayfirst=True,errors="coerce")

    gastos = df[df["Amount"]<0]
    ingresos = df[df["Amount"]>0]

    st.subheader("Gastos por categoría")

    cat = gastos.groupby("Category")["Amount"].sum().reset_index()

    fig1 = px.pie(cat,values="Amount",names="Category")

    st.plotly_chart(fig1)

    st.subheader("Flujo de dinero")

    trend = df.groupby("Date")["Amount"].sum().reset_index()

    fig2 = px.line(trend,x="Date",y="Amount")

    st.plotly_chart(fig2)

    total_ingresos = ingresos["Amount"].sum()
    total_gastos = gastos["Amount"].sum()
    balance = total_ingresos + total_gastos

    fig3 = go.Figure(go.Waterfall(
        x=["Ingresos","Gastos","Balance"],
        y=[total_ingresos,total_gastos,balance]
    ))

    st.subheader("Balance")

    st.plotly_chart(fig3)
