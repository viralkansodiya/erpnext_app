frappe.ui.form.on("Quotation", {
    refresh:(frm)=>{
        console.log('refresh')
    }
})

frappe.ui.form.on("Quotation Item", {
    percentage:(frm, cdt, cdn)=>{
        let d = locals[cdt][cdn]
        calculate_service_item_rate(frm, cdt , cdn)
    },
    rate:(frm, cdt, cdn)=>{
        let d = locals[cdt][cdn]
        calculate_service_item_rate(frm, cdt , cdn)
    },
    qty:(frm, cdt, cdn)=>{
        let d = locals[cdt][cdn]
        calculate_service_item_rate(frm, cdt , cdn)
    },
    discount_percentage:(frm, cdt, cdn)=>{
        let d = locals[cdt][cdn]
        calculate_service_item_rate(frm, cdt , cdn)
    },
    discount_amount:(frm, cdt, cdn)=>{
        let d = locals[cdt][cdn]
        calculate_service_item_rate(frm, cdt , cdn)
    },

})
function calculate_service_item_rate(frm, cdt, cdn){
    let d = locals[cdt][cdn]
    if(!d.percentage) return;
    frappe.call({
        method: "custom_app.doc_events.quotation.get_service_item_rate",
        args : {
            doc : frm.doc,
            percentage : d.percentage,
            item_code : d.item_code
        },
        callback:(r)=>{
            if(r.message){
                frappe.model.set_value(cdt, cdn, "rate", r.message)
                frm.refresh_field("items")
            }
        }
    })
}