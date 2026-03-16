import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Mi dashboard financiero")

archivo=st.file_uploader("Sube tu archivo de Budge (CSV o Excel)")

if archivo is not None:
if archivo.name.endswith(".csv"):
  df=pd.read_csv(archivo,encoding="latin1",sep=",")
 else:
  df=pd.read_excel(archivo)

 if df.shape[1]==1:
  df=df[df.columns[0]].str.split(",",expand=True)

 df.columns=["Date","Payment","IsPaid","Amount","Currency","Account","Category","Subcategory","Goal","Description"]

 df["Amount"]=pd.to_numeric(df["Amount"],errors="coerce")
 df["Date"]=pd.to_datetime(df["Date"],errors="coerce")

 st.subheader("Filtros")

 categorias=df["Category"].dropna().unique()

 categoria_filtro=st.multiselect("Selecciona categoría",categorias,default=categorias)

 df=df[df["Category"].isin(categoria_filtro)]

 col1,col2,col3=st.columns(3)

 ingresos=df[df["Amount"]>0]["Amount"].sum()
 gastos=df[df["Amount"]<0]["Amount"].sum()
 balance=ingresos+gastos

 col1.metric("Ingresos",f"${ingresos:,.0f}")
 col2.metric("Gastos",f"${gastos:,.0f}")
 col3.metric("Balance",f"${balance:,.0f}")

 st.subheader("Gastos por categoría")

 resumen=df.groupby("Category")["Amount"].sum().reset_index()

 fig1=px.bar(resumen,x="Category",y="Amount")

 st.plotly_chart(fig1,use_container_width=True)

 st.subheader("Flujo de dinero")

 flujo=df.groupby("Date")["Amount"].sum().reset_index()

 fig2=px.line(flujo,x="Date",y="Amount")

 st.plotly_chart(fig2,use_container_width=True)

 st.subheader("Presupuesto por categoría")

 presupuesto={}

 for c in categorias:
  presupuesto[c]=st.number_input(f"Presupuesto {c}",value=0)

 tabla_presupuesto=pd.DataFrame(list(presupuesto.items()),columns=["Category","Budget"])

 comparacion=resumen.merge(tabla_presupuesto,on="Category",how="left")

 comparacion["Ejecutado"]=comparacion["Amount"].abs()

 comparacion["Diferencia"]=comparacion["Budget"]-comparacion["Ejecutado"]

 st.subheader("Presupuesto vs ejecutado")

 st.dataframe(comparacion)

 for i in comparacion.index:

  if comparacion.loc[i,"Budget"]>0:

   uso=comparacion.loc[i,"Ejecutado"]/comparacion.loc[i,"Budget"]

   if uso>1:
    st.error(f"⚠️ Excediste el presupuesto en {comparacion.loc[i,'Category']}")

   elif uso>0.8:
    st.warning(f"⚠️ Has usado más del 80% en {comparacion.loc[i,'Category']}")

 st.subheader("Balance")

 balance_df=pd.DataFrame({
 "Tipo":["Ingresos","Gastos","Balance"],
 "Valor":[ingresos,abs(gastos),balance]
 })

 fig3=px.bar(balance_df,x="Tipo",y="Valor")

 st.plotly_chart(fig3,use_container_width=True)
