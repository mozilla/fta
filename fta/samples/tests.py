from bs4 import BeautifulSoup

from .utils import convert_fathom_sample_to_labeled_sample

PAGE_BEGIN = (
    '<html lang="en-us">'
    '<head><meta charset="utf-8"/>'
    "<title>Title</title>"
    '<body class="app-polls model-question change-list">'
)
PAGE_END = "</body></html>"
SEARCH_FATHOM_LABEL = (
    '<input data-fathom="search" id ="searchbar" name="q" type="text" value=' "/>"
)
EMAIL_FATHOM_LABEL = (
    '<input data-fathom="email" id="id2" name="question_text" type="text" value=' "/>"
)
NO_LABEL = '<input id="id_question_text" name="question_text" type="text" value=' "/>"
WITH_FTA_ID = '<input data-fta_id="1234" id="id1" name="n" type="text" value=' "/>"


def test_convert_fathom_sample_to_labeled_sample_1():
    page = PAGE_BEGIN + SEARCH_FATHOM_LABEL + NO_LABEL + WITH_FTA_ID + PAGE_END
    labeled_sample, labels_to_fta_id = convert_fathom_sample_to_labeled_sample(page)
    assert len(labels_to_fta_id) == 1
    assert "search" in labels_to_fta_id
    assert labels_to_fta_id["search"] is not None

    # check that the html has 1 data-fta_id entry, not 2
    soup = BeautifulSoup(labeled_sample, features="html.parser")
    fta_labeled_elements = [
        item for item in soup.find_all() if "data-fta_id" in item.attrs
    ]
    assert len(fta_labeled_elements) == 1


def test_convert_fathom_sample_to_labeled_sample_2():
    page = (
        PAGE_BEGIN + SEARCH_FATHOM_LABEL + EMAIL_FATHOM_LABEL + WITH_FTA_ID + PAGE_END
    )
    labeled_sample, labels_to_fta_id = convert_fathom_sample_to_labeled_sample(page)
    assert len(labels_to_fta_id) == 2
    assert "search" in labels_to_fta_id
    assert "email" in labels_to_fta_id
    assert labels_to_fta_id["search"] is not None
    assert labels_to_fta_id["email"] is not None
    assert labels_to_fta_id["search"] is not labels_to_fta_id["email"]

    # check that the html has 2 data-fta_id entry, not 3
    soup = BeautifulSoup(labeled_sample, features="html.parser")
    fta_labeled_elements = [
        item for item in soup.find_all() if "data-fta_id" in item.attrs
    ]
    assert len(fta_labeled_elements) == 2
