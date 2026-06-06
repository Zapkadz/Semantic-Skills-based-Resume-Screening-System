"""Streamlit entry point for the Semantic Skills resume screening project.

Phase 01 only provides a placeholder page. The functional UI is planned for a
later phase after the core screening flow is available.
"""

from __future__ import annotations


PROJECT_NAME = "Semantic Skills-based Resume Screening System"
CURRENT_PHASE = "Phase 01 - Project Foundation"


def main() -> None:
    """Render the minimal Streamlit placeholder."""
    try:
        import streamlit as st
    except ModuleNotFoundError:
        print("Streamlit is not installed yet.")
        print("Run: pip install -r requirements.txt")
        return

    st.set_page_config(page_title="Semantic Skills Resume Screening")
    st.title(PROJECT_NAME)
    st.caption(CURRENT_PHASE)
    st.info(
        "The repository foundation is ready. Resume screening features will be "
        "implemented in later phases."
    )


if __name__ == "__main__":
    main()
