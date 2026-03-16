import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Mi dashboard financiero")

archivo=st.file_uploader("Sube tu archivo de Budge (CSV o Excel)")

if archivo is not None:

try:
df=pd.read_csv(archivo,encoding="latin1")
except:
df=pd.read_excel(archivo)

if df.shape[1]==1:
df=df.iloc[:,0].str.split(",",expand=True)
df.columns=["Date","Payment","IsPaid","Amount","Currency","Account","Category","Subcategory","Note"]

df["Amount"]=pd.to_numeric(df["Amount"],errors="coerce")
df["Date"]=pd.to_datetime(df["Date"],errors="coerce")

st.subheader("Filtro")

categorias=df["Category"].dropna().unique()

categoria=st.selectbox("Selecciona categoría",["Todas"]+list(categorias))

if categoria!="Todas":
df=df[df["Category"]==categoria]

st.subheader("Gastos por categoría")

resumen=df.groupby("Category")["Amount"].sum().reset_index()

fig=px.pie(resumen,values="Amount",names="Category")

st.plotly_chart(fig)

st.subheader("Flujo de dinero")

flujo=df.groupby("Date")["Amount"].sum().reset_index()

fig2=px.line(flujo,x="Date",y="Amount")

st.plotly_chart(fig2)

st.subheader("Balance")

ingresos=df[df["Amount"]>0]["Amount"].sum()
gastos=df[df["Amount"]<0]["Amount"].sum()
balance=ingresos+gastos

balance_df=pd.DataFrame({
"Tipo":["Ingresos","Gastos","Balance"],
"Valor":[ingresos,gastos,balance]
})

fig3=px.bar(balance_df,x="Tipo",y="Valor")

st.plotly_chart(fig3)
