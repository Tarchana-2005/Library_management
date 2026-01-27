frappe.ui.form.on('Library Member', {
 refresh: function(frm) {
 frm.add_custom_button('Create Membership', () => {
 frappe.new_doc('Library Membership', {
 library_member: frm.doc.name
 })
 })

 frm.add_custom_button('Create Transaction', () => {
 frappe.new_doc('Library Transaction', {
 library_member: frm.doc.name
 })
 })
 }
});

frappe.ui.form.on('Library Member', {
 refresh: function(frm) {
frm.add_custom_button('View Issued Books', () => {
    frappe.set_route('query-report', 'Member-wise Transaction Report', {
        library_member : frm.doc.name,
        issue_transaction: "not_set"
    });
});
 }
})

// frappe.ui.form.on("Library Member", {
//     refresh: function(frm) {
//         if (!frm.is_new()) {
//             frm.add_custom_button("View Issued Books", function() {
//                 show_issued_books(frm);
//             });
//         }
//     }

// });


// function show_issued_books(frm) {
//     frappe.call({
//         method: "library_management.library_management.doctype.library_transaction.library_transaction.get_member_issued_books",
//         args: {
//             member: frm.doc.name
//         },
//         callback: function(r) {

//             if (r.message && r.message.length > 0) {

//                 show_dialog(r.message);

//             } else {

//                 frappe.msgprint("No issued books found for this member.");
//             }
//         }
//     });
// }


// function show_dialog(data) {
//     let html = `
//         <table class="table table-bordered">
//             <thead>
//                 <tr>
//                     <th>Article</th>
//                     <th>Issue Date</th>
//                 </tr>
//             </thead>
//             <tbody>
//     `;

//     data.forEach(row => {

//         html += `
//             <tr>
//                 <td>${row.article}</td>
//                 <td>${row.date}</td>
//             </tr>
//         `;
//     });

//     html += `
//             </tbody>
//         </table>
//     `;

//     let d = new frappe.ui.Dialog({
//         title: "Issued Books",
//         fields: [
//             {
//                 fieldtype: "HTML",
//                 fieldname: "issued_books",
//                 options: html
//             }
//         ],
//         size: "large"
//     });

//     d.show();
// }
