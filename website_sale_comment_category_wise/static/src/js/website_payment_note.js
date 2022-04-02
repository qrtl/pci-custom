odoo.define("website_sale_comment_category_wise.payment", function (require) {
    "use strict";

    var ajax = require("web.ajax");
    $(document).ready(function () {
        $("#order_comment")
            .find("[name='note']")
            .on("change", function () {
                ajax.jsonRpc("/shop/order/note", "call", {
                    note: $(this).val(),
                });
            });
    });
});
