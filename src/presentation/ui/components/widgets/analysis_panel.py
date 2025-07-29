import streamlit as st
from application.dtos.analysis_dto import AnalysisDTO
from presentation.ui.utils.localization import get_localizer

class AnalysisPanel:
    def render(self, analysis_dto: AnalysisDTO):
        t = get_localizer()
        st.header(t("analysis_results_header"))

        # Technical Analysis Section
        with st.container(border=True):
            st.subheader(t("technical_summary_header"))
            tech_analysis = analysis_dto.technical_analysis
            
            col1, col2, col3 = st.columns(3)
            col1.metric(t("trend_metric"), tech_analysis.trend.capitalize())
            col2.metric(t("strength_metric"), f"{tech_analysis.strength:.2f}")
            col3.metric(t("recommendation_metric"), tech_analysis.recommendation)

            with st.expander(t("signals_expander")):
                if tech_analysis.signals:
                    for signal in tech_analysis.signals:
                        st.info(signal)
                else:
                    st.write(t("no_signals"))

        st.write("") # Spacer

        # AI Analysis Section
        with st.container(border=True):
            st.subheader(t("ai_insights_header"))
            ai_analysis = analysis_dto.ai_analysis

            if ai_analysis:
                st.metric(t("ai_recommendation_metric"), ai_analysis.get("recommendation", "N/A"), delta=ai_analysis.get("confidence", ""))
                
                st.write(f'**{t("summary_header")}**')
                st.write(ai_analysis.get("summary", "No summary available."))

                with st.expander(t("detailed_analysis_expander")):
                    detailed = ai_analysis.get("detailed_analysis", {})
                    for key, value in detailed.items():
                        st.write(f"**{key.replace('_', ' ').title()}:**")
                        st.write(value)
            else:
                st.warning("AI analysis is not available.")
