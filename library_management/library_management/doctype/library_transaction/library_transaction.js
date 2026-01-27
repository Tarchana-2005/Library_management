// frappe.ui.form.on('Library Transaction', {
//     library_member: set_issue_transaction,
//     type: set_issue_transaction,

//     set_issue_transaction(frm) {

//         if (frm.doc.type !== "Return" || !frm.doc.library_member) {
//             frm.set_value("issue_transaction", "");
//             return;
//         }

//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Library Transaction",
//                 filters: {
//                     library_member: frm.doc.library_member,
//                     type: "Issue",
//                     docstatus: 1,
//                     is_returned: 0
//                 },
//                 fields: ["name", "article"],
//                 order_by: "creation desc",
//                 limit_page_length: 1
//             },
//             callback(r) {
//                 if (r.message && r.message.length) {
//                     frm.set_value("issue_transaction", r.message[0].name);
//                     frm.set_value("article", r.message[0].article);
//                 } else {
//                     frm.set_value("issue_transaction", "");
//                     frappe.msgprint("No active issue found for this member");
//                 }
//             }
//         });
//     }
// });
