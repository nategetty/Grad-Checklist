function includeHtml() {
    $("[data-include]").each((index, element) => {
        $.get("include/" + $(element).data("include"), (data) => {
            $(element).replaceWith(data)
        });
    });
}