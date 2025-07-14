import datetime as dt
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import streamlit_shadcn_ui as ui
from PIL import Image
import time
from capm import CAPM

def main():
    im = Image.open("capm_img.png")

    st.set_page_config(page_title="Capital Asset Pricing Model", page_icon=im)

    st.markdown("## Capitsal Asset Pricing Model")
    col1, col2 = st.columns([0.14, 0.86], gap="small")
    col1.write("`Created by: `")
    linkedin_url = "https://www.linkedin.com/in/edijemeni/"
    col2.markdown(
        f'<a href="{linkedin_url}"> Esuabom Dijemeni </a>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([0.14, 0.86], gap="small")
    col1.write("`Code at: `")
    github_url = "https://github.com/cmj123/capm"
    col2.markdown(
        f'<a href="{github_url}"> CAPM GitHub Code </a>',
        unsafe_allow_html=True,
    )
    

    st.markdown("CAPM is a financial model that calculates the expected rate of return for an asset or investment.CAPM does this by using the expected return on both the market and a risk-free asset, and the asset’s correlation or sensitivity to the market (beta).")

   
    cont1 = st.container(border=True)
    cont1.markdown("### Input Parameter")
    # stock = cont1.text_input(
    #     "Enter Ticker", value="AAPL",
    # )

    # benchmark = cont1.text_input(
    #     "Enter Benchmark", value="^GSPC",
    # )

    stock, benchmark = cont1.columns(2)
    stock = stock.text_input(
        "Enter Ticker", value="AAPL",
    )

    benchmark = benchmark.text_input(
        "Enter Benchmark", value="^GSPC",
    )


    start, end = cont1.columns(2)
    start_date = start.date_input(
        "Start Date",
        max_value=dt.date.today() - dt.timedelta(days=1),
        min_value=dt.date.today() - dt.timedelta(days=3650),
        value=dt.date.today() - dt.timedelta(days=3650)
    )

    end_date = end.date_input(
        "End Date",
        max_value=dt.date.today(),
        min_value=start_date + dt.timedelta(days=1),
        value=dt.date.today(),
    )

    calc = cont1.button("Run")

    if calc:
        try:
            with st.spinner("CAPM analysis in progess"):
                time.sleep(2)
                capm = CAPM([stock, benchmark], start_date, end_date)
                capm.initialize()
                capm.regression()

        except:
            st.error("Wrong Input")
        
        with st.container(border=True):
            tab1, tab2, tab3 = st.tabs(
                [
                    "CAPM",
                    "Summary",
                    "Dataset"
                ]
            )
            with tab2:
                st.markdown("#### Summary")
                st.markdown(f"**Expected Return**: {capm.expected_return*100:.2f}%")
                st.markdown(f"**Beta**: {capm.beta:.4f}")
                st.markdown(f"**Market Return**: {capm.market_return*100:.2f}%")
                st.markdown(f"**Market Risk Premium**: {capm.market_risk_premium*100:.2f}%")
                st.markdown(f"**Risk Free Rate**: {1.00:.2f}%")
                

            with tab1:
                st.markdown("#### CAPM GRAPH")
                            
                # # Plot figure
                # fig, axis = plt.subplots(1, figsize=(10,6))
                # axis.scatter(capm.data["m_returns"], capm.data['s_returns'], label="Data Points")
                # axis.plot(capm.data["m_returns"], capm.beta*capm.data["m_returns"] + capm.alpha, color='red', label="CAPM Line")
                # plt.title('Capital Asset Pricing Model, finding alpha and beta')
                # plt.xlabel('Market return $R_m$')
                # plt.ylabel('Stock return $R_a$')
                # # plt.text(0.8, 0.15, er_beta_str , horizontalalignment='right', verticalalignment='top', transform=axis.transAxes)
                # plt.legend()
                # plt.grid(True)
                # # plt.show()
                # st.pyplot(fig)

                ## Plot Grpah
                capm.data["m_returns"] = capm.data["m_returns"]*100
                capm.data["s_returns"] = capm.data["s_returns"]*100
                capm.data["expected_return"]=capm.beta*capm.data["m_returns"] + capm.alpha
                fig3 = go.Figure()
                fig3.add_trace(
                    go.Scatter(
                        x=capm.data["m_returns"], 
                        y=capm.data["s_returns"], 
                        mode='markers', 
                        name="Returns",
                        line=dict(color='blue')
                    ),
                )
                fig3.add_trace(
                    go.Scatter(
                        x=capm.data["m_returns"], 
                        y=capm.data["expected_return"], 
                        mode="lines+markers",
                        name="CAPM Line",
                        line=dict(color='red')
                    )
                )

                fig3.update_xaxes(title_text = "Market Return (%)")
                fig3.update_yaxes(title_text = "Expected Return (%)")
                fig3.update_layout(title = dict(text="Capital Asset Pricing Model"),legend_title_text = "Result")
              
                st.plotly_chart(fig3, use_container_width=True)

            with tab3:
                st.markdown("#### Dataset")
                st.dataframe(capm.data)


if __name__ == "__main__":
    main()