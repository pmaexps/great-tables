from __future__ import annotations

from typing import TYPE_CHECKING

from ._locations import Loc, PlacementOptions, set_footnote, set_style
from ._styles import CellStyle


if TYPE_CHECKING:
    from ._types import GTSelf


def tab_style(
    self: GTSelf, style: CellStyle | list[CellStyle], locations: Loc | list[Loc]
) -> GTSelf:
    """Add custom style to one or more cells

    With the `tab_style()` method we can target specific cells and apply styles to them. We do this
    with the combination of the `style` and `location` arguments. The `style` argument requires use
    of styling classes (e.g., `style.fill(color="red")`) and the `location` argument needs to be an
    expression of the cells we want to target using location targeting classes (e.g.,
    `loc.body(columns=<column_name>)`). With the available suite of styling classes, here are some
    of the styles we can apply:

    - the background color of the cell (`style.fill()`'s `color`)
    - the cell's text color, font, and size (`style.text()`'s `color`, `font`, and `size`)
    - the text style (`style.text()`'s `style`), enabling the use of italics or oblique text.
    - the text weight (`style.text()`'s `weight`), allowing the use of thin to bold text (the degree
    of choice is greater with variable fonts)
    - the alignment and indentation of text (`style.text()`'s `align` and `indent`)
    - cell borders with the `style.borders()` class

    Parameters
    ----------
    style : CellStyle | list[CellStyle]
        The styles to use for the cells at the targeted `locations`. The `style.text()`,
        `style.fill()`, and `style.borders()` classes can be used here to more easily generate valid
        styles.
    location : Loc | list[Loc]
        The cell or set of cells to be associated with the style. The `loc.body()` class can be used
        here to easily target body cell locations.

    Examples
    --------
    Let's use a small subset of the `exibble` dataset to demonstrate how to use `tab_style()` to
    target specific cells and apply styles to them. We'll start by creating the `exibble_sm` table
    (a subset of the `exibble` table) and then use `tab_style()` to apply a light cyan background
    color to the cells in the `num` column for the first two rows of the table. We'll then apply a
    larger font size to the cells in the `fctr` column for the last four rows of the table.

    ```{python}
    import great_tables as gt
    from great_tables import style, loc
    from great_tables import exibble

    exibble_sm = exibble[["num", "fctr", "row", "group"]]

    (
        gt.GT(exibble_sm, rowname_col="row", groupname_col="group")
        .tab_style(
            style=style.fill(color="lightcyan"),
            locations=loc.body(columns="num", rows=["row_1", "row_2"]),
        )
        .tab_style(
            style=style.text(size="22px"),
            locations=loc.body(columns=["fctr"], rows=[4, 5, 6, 7]),
        )
    )
    ```

    Returns
    -------
    GT
        The GT object is returned.
    """

    if not isinstance(style, list):
        style = [style]

    if not isinstance(locations, list):
        locations = [locations]

    new_data = self
    for loc in locations:
        new_data = set_style(loc, self, style)

    return new_data


# TODO: note that this function does not yet render, and rendering
# will likely be implemented down the road (e.g. after basic styling).
# this is just all the machinery to set data in GT._footnotes
def tab_footnote(
    self: GTSelf,
    footnote: str | list[str],
    locations: Loc | None | list[Loc | None],
    placement: PlacementOptions = "auto",
) -> GTSelf:
    """Add a footnote to a table

    Parameters
    ----------
    footnote:
        The footnote text.
    locations:
        The location to place the footnote. If None, then a footnote is created without
        a correesponding marker on the table (TODO: double check this).
    placement:
        Where to affix the footnote marks to the table content.

    """

    if isinstance(footnote, list):
        raise NotImplementedError("Currently, only a single string is supported for footnote.")

    if not isinstance(locations, list):
        locations = [locations]

    new_data = self
    if isinstance(locations, list):
        for loc in locations:
            new_data = set_footnote(loc, self, footnote, placement)

    return new_data
