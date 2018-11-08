jQuery(function($) {
    $(document).ready(function() {
        $(".copy_data").unbind('click');
        $(".copy_data").click(function(ev) {
            ev.preventDefault();
            var url=$(this).data("form");
            $("#copyModal").load(url, function() {
                $("#copyModal").modal('show');
                $(document).click(function(event) {
                    if (! $(event.target).closest(".modal-dialog").length) {
                    	$("#copyModal").modal('hide');
                    }
                });
            });
            return false;
        });
    });
});
