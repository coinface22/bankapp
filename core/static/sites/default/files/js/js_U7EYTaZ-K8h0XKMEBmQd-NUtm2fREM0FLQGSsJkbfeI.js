jQuery(document).ready(function ($) {
  // Collect all footnotes on the page and add to #footnotes-all block.
  const $globalWrapper = $('[drupal-data-selector="footnotes-all"]');
  const $footnotesList = $('[drupal-data-selector="footnotes-global-list"]');
  if ($globalWrapper) {
    const $footnotes = $("ul.footnotes").not(
      '[drupal-data-selector="footnotes-global-list"]'
    );
    if ($footnotes.length) {
      $globalWrapper.removeClass("visually-hidden");
    }
    var lastLabel = 0;
    $footnotes.once("globalFootnotes").each(function () {
      // Fix any duplicate footnote labels. Can happen for embedded rendered entities that do not have the context of the parent content.
      const $el = $(this);
      const $labels = $el.find("li a.footnote-label");
      $labels.each(function () {
        const $label = $(this);
        const $parent = $($label.attr("href"));
        var labelNumber = parseInt($parent.text());
        if (labelNumber != NaN) {
          if (lastLabel + 1 != labelNumber) {
            labelNumber = lastLabel + 1;
            $parent.text(labelNumber);
            $label.text(labelNumber);
          }
          lastLabel = labelNumber;
        }
      });
      if ($globalWrapper) {
        $footnotesList.append($el.html());
        $el.remove();
      }
    });
    // Consolidate duplicate disclosure text.
    var newList = [];
    var textIndex = [];
    $footnotesList.find("li").each(function () {
      var text = $(this).find("span").text();
      var foundItem = textIndex.indexOf(text);
      if (foundItem > -1) {
        var link = $(this).find("a").first();
        $foundEl = $(newList[foundItem]);
        link.attr("id", $(this).attr("id"));
        var linkWrapper = $foundEl.find(".footnotes-add-references");
        if (!linkWrapper.length) {
          $foundEl
            .find("span")
            .first()
            .before('<span class="footnotes-add-references"></span>');
          linkWrapper = $foundEl.find(".footnotes-add-references");
        }
        linkWrapper.append(link);
      } else {
        var index = newList.push($(this).clone());
        textIndex[index - 1] = text;
      }
    });
    if (newList.length != $footnotesList.find("li").length) {
      $footnotesList.html(newList);
    }
  }
  $(window).trigger("footnotesComplete");
});
;
