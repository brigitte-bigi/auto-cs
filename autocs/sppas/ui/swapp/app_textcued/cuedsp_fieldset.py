"""
:filename: annotate_page.cuedsp_fieldset.py
:author: Brigitte Bigi
:contributor: Florian Lopitaux
:contact: contact@sppas.org
:summary: Cuedspeech fieldset of the annotate page.

.. _This file is part of AutoCuedSpeech: <https://auto-cuedspeech.org/>
.. _Originally developed in SPPAS: <https://sppas.org/>
..
    ---------------------------------------------------------------------

    Copyright (C) 2011-2025  Brigitte Bigi, CNRS
    Laboratoire Parole et Langage, Aix-en-Provence, France

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    This banner notice must not be removed.

    -------------------------------------------------------------------------

"""

from __future__ import annotations
import ast

from whakerpy.htmlmaker import HTMLNode

from sppas.core.config import separators
from sppas.ui import _

from .text2cue import TextToCues
from .annotate_view import SPPASAnnotateNode

# ---------------------------------------------------------------------------


MSG_FIELD_LEGEND = _("Sequence of phonemes to be cued")
MSG_BREADCRUMB = _("Phonetized text")
MSG_ANN_NAME = _("Convert phonemes into CS keys")
MSG_PREV_INPUT = _("See the text previously normalized")
MSG_TEXT = _("Choose or add the pronunciation of each word to be automatically coded: ")
MSG_SAMPA = _(":INFO 9898: ")

MSG_REF = _("Bibliographical references")

# ---------------------------------------------------------------------------


HTML_REFERENCE = """
        <h2>{:s}</h2>

        <blockquote><p>
            Brigitte Bigi (2023).
            <a class="external-link" href="https://hal.science/hal-04081282">
            An analysis of produced versus predicted French Cued Speech keys.
            </a>
            In 10th Language & Technology Conference: Human Language Technologies
            as a Challenge for Computer Science and Linguistics,
            ISBN: 978-83-232-4176-8, pp. 24-28, Poznań, Poland.
        </p>
        </blockquote>
        <blockquote><p>
            Núria Gala, Brigitte Bigi, Marie Bauer (2024).
            <a class="external-link" href="https://hal.science/hal-04580180">
            Automatically Estimating Textual and Phonemic Complexity for Cued Speech:
            How to See the Sounds from French Texts</a>
            In the 2024 Joint International Conference on Computational Linguistics,
            Language Resources and Evaluation (LREC-COLING), pp. 1817-1824, Turin, Italy.</a>
        </p>
        </blockquote>
""".format(MSG_REF)

# ---------------------------------------------------------------------------


class CuedspeechFieldset(SPPASAnnotateNode):
    """CuedSpeech automatic annotation.

    Requires phonetized tokens. Perform alignment automatic annotation.
    Produces a sequence of key codes.

    """

    def __init__(self, parent_id: str):
        super(CuedspeechFieldset, self).__init__(parent_id, "cuedspeech", MSG_BREADCRUMB, MSG_FIELD_LEGEND)
        self.set_attribute("id", "cuedspeech")
        self._btn_text = MSG_ANN_NAME

    # ---------------------------------------------------------------------------

    @staticmethod
    def serialize_ann_result(result) -> str:
        """Override. Convert the annotation result into a string.

        :param result: list(tuple(keys,phones)
        :return: (str) a string sequence of keys

        """
        return TextToCues.serialize_cued(result)

    # -----------------------------------------------------------------------

    @staticmethod
    def format_ann_result(result) -> str:
        """Override. Convert the annotation result into an input for the result.

        :param result: list[tuple(keys,phones)]
        :return: (str)

        """
        return TextToCues.format_cued(result)

    # ---------------------------------------------------------------------------
    # PUBLIC METHODS
    # ---------------------------------------------------------------------------

    def set_phon(self, token: str, phon: str):
        pass

    # ---------------------------------------------------------------------------
    # Override from SPPASAnnotateNode
    # ---------------------------------------------------------------------------

    def _fill_content_form(self) -> None:
        """To be documented.

        """
        # Annotation language
        self._lang_choices(self._set_lang_choices())

        # Annotation input
        label = HTMLNode(self._form.identifier, None, "label",
                         attributes={"for": self.identifier + "_input_text"}, value=MSG_TEXT)
        self._form.append_child(label)
        # the table content is the current input in result, if exists.
        if self.identifier in self._ann_results:
            r = self._ann_results[self.identifier]
            if len(r[1]) > 0:
                ast_r = ast.literal_eval(r[1])
                self.__create_phon_table(ast_r)

        # Annotation information
        p = HTMLNode(self._form.identifier, None, "p", value=MSG_SAMPA)
        self._form.append_child(p)

    # ---------------------------------------------------------------------------

    @staticmethod
    def annotate(text: str, lang: str = "und") -> list:
        """Override. Return the result of "CuedSpeech" on the given phonetized text.

        :param text: (str) Input phonetized text to be cued
        :param lang: (str) Language of the rules for cueing (iso639-1)
        :return: (list) List of keys

        """
        annotator = TextToCues(lang)
        aligned = annotator.aligner(text)
        return annotator.cuer(aligned)

    # -----------------------------------------------------------------------

    def _create_extra_content(self) -> None:
        """Override. Create any content to be added below the form.

        """
        section = HTMLNode(self.identifier, "references", "section", value=HTML_REFERENCE)
        self.append_child(section)

    # ---------------------------------------------------------------------------
    # PRIVATE METHODS
    # ---------------------------------------------------------------------------

    def __create_phon_table(self, ann_results: list[tuple]) -> None:
        """To be documented.

        """
        # create table
        table = HTMLNode(self._form.identifier, "table-phonemes", "table", attributes={'role': "grid", 'class': "cuedsp-form"})
        self._form.append_child(table)

        # create first row with column names (thead element)
        thead = HTMLNode(table.identifier, "table-head", "thead")
        table.append_child(thead)
        head_row = HTMLNode(thead.identifier, "head-row", "tr")
        thead.append_child(head_row)

        token_th = HTMLNode(head_row.identifier, None, "th", value="Tokens", attributes={'scope': "col", 'style': "width:15%"})
        phon1_th = HTMLNode(head_row.identifier, None, "th", value="Choix n°1", attributes={'scope': "col", 'style': "width:10%"})
        phon2_th = HTMLNode(head_row.identifier, None, "th", value="Choix n°2", attributes={'scope': "col", 'style': "width:10%"})
        phon3_th = HTMLNode(head_row.identifier, None, "th", value="Choix n°3", attributes={'scope': "col", 'style': "width:10%"})
        phon4_th = HTMLNode(head_row.identifier, None, "th", value="Choix n°4", attributes={'scope': "col", 'style': "width:10%"})
        input_th = HTMLNode(head_row.identifier, None, "th", value="Personalisé", attributes={'scope': "col", 'style': "width:15%"})
        head_row.append_child(token_th)
        head_row.append_child(phon1_th)
        head_row.append_child(phon2_th)
        head_row.append_child(phon3_th)
        head_row.append_child(phon4_th)
        head_row.append_child(input_th)

        # create rows for each phon token
        tbody = HTMLNode(table.identifier, "table-body", "tbody")
        table.append_child(tbody)

        for index, element in enumerate(ann_results):
            if len(element) < 2:
                return

            # get token and phonemes list
            token = element[0].replace("%27", "'")
            phonemes = element[1].replace("%27", "'").split(separators.variants)

            # create row and first&second column
            current_row = HTMLNode(tbody.identifier, f"row-{token}", "tr")
            tbody.append_child(current_row)

            current_token = HTMLNode(current_row.identifier, None, "th", value=token, attributes={'scope': 'row'})
            current_row.append_child(current_token)

            # append phonemes cell. the default selected variant is the first shortest one.
            self.__create_phon_cells(current_row, index, token, phonemes)

            # create phon input
            input_td = HTMLNode(current_row.identifier, f"{token}-{index}_phon_td", "td")
            phon_input = HTMLNode(input_td.identifier, None, "input", attributes={
                'id': f"{token}-{index}_phon_input",
                'name': f"{token}-{index}_phon_input",
                'class': "phon_input",
                'onchange': "input_onchange(this)"
            })

            current_row.append_child(input_td)
            input_td.append_child(phon_input)

    # ---------------------------------------------------------------------------

    def __create_phon_cells(self, row: HTMLNode, token_index: int, token: str, phonemes: list[str], chosen: int = 0) -> None:
        """To be documented.

        """
        # Sort phonemes: from shortest to longest
        sorted_phonemes = sorted(phonemes, key=lambda s: len(s.split('-')))

        # Create 4 cells for a current row
        for i in range(4):
            phon_cell = HTMLNode(row.identifier, f"{token}-{token_index}_cell_{i}", "td")
            row.append_child(phon_cell)

            if len(sorted_phonemes) >= i + 1:
                phon_btn = HTMLNode(phon_cell.identifier, None, "button", value=sorted_phonemes[i], attributes={
                    'name': f"{token}-{token_index}_button",
                    'onclick': "select_token_phon(this);",
                    'onkeydown': "select_token_phon(this);"
                })
                if chosen == i:
                    phon_btn.set_attribute("class", f"phon_chosen")
                    phon_btn.set_attribute("disabled", "")
                else:
                    phon_btn.set_attribute("class", f"phon_not_chosen")

                phon_cell.append_child(phon_btn)
