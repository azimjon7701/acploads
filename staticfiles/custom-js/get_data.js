function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

function check_data(data) {
    return data ? data : '-'
}

function render_contact_by_type(type, data) {
    if (type === 'telegram') {
        contact_link = data.startsWith('@') ? data.slice(1) : data
        contact = data.startsWith('@') ? data : '@' + data
        return `<i class=" c-theme-font" style="color: #4b4545 !important;"><svg style="top: 3px; position: relative;" xmlns="http://www.w3.org/2000/svg" width="22" height="16" fill="currentColor" class="bi bi-telegram" viewBox="0 0 16 16">
                                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.287 5.906c-.778.324-2.334.994-4.666 2.01-.378.15-.577.298-.595.442-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294.26.006.549-.1.868-.32 2.179-1.471 3.304-2.214 3.374-2.23.05-.012.12-.026.166.016.047.041.042.12.037.141-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8.154 8.154 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629.093.06.183.125.27.187.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.426 1.426 0 0 0-.013-.315.337.337 0 0 0-.114-.217.526.526 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09z"></path>
                            </svg></i><a class="contact-link" target="_blank" href = "https://t.me/${contact_link}"> ${contact} </a>`
    } else if (type === 'phone') {
        return `<i class="c-theme-font" style="color: #4b4545 !important;">
                            <svg style="top: 3px; position: relative;"  xmlns="http://www.w3.org/2000/svg" width="22" height="16" fill="currentColor" class="bi bi-telephone-fill" viewBox="0 0 16 16">
                                <path fill-rule="evenodd" d="M1.885.511a1.745 1.745 0 0 1 2.61.163L6.29 2.98c.329.423.445.974.315 1.494l-.547 2.19a.678.678 0 0 0 .178.643l2.457 2.457a.678.678 0 0 0 .644.178l2.189-.547a1.745 1.745 0 0 1 1.494.315l2.306 1.794c.829.645.905 1.87.163 2.611l-1.034 1.034c-.74.74-1.846 1.065-2.877.702a18.634 18.634 0 0 1-7.01-4.42 18.634 18.634 0 0 1-4.42-7.009c-.362-1.03-.037-2.137.703-2.877L1.885.511z"></path>
                            </svg>
                        </i>&ensp; <a class="contact-link" target="_blank" href="tel:${data}">${data}</a>
                        `
    } else if (type === 'email') {
        return `<i class="c-theme-font" style="color: #4b4545 !important;">
                            <svg style="top: 3px; position: relative;"  xmlns="http://www.w3.org/2000/svg" width="22" height="16" fill="currentColor" class="bi bi-envelope-fill" viewBox="0 0 16 16">
                                <path d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414.05 3.555ZM0 4.697v7.104l5.803-3.558L0 4.697ZM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586l-1.239-.757Zm3.436-.586L16 11.801V4.697l-5.803 3.546Z"></path>
                            </svg>
                        </i>&ensp; <a class="contact-link" target="_blank" href="mailto:${data}" >${data}</a>
        `
    } else {
        return '-'
    }
}

function post_data_fetch(url, data, callback) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'reciver_id': 'reciver_id'})
    })
        .then((response) => {
            response.json().then((data) => {
                console.log(data)
            })
        })
}

function post_data(url, data, callback) {
    $.ajax({
        type: "POST",
        contentType: "application/json",
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: url,
        headers: {
            'X-CSRF-TOKEN': getCookie('csrftoken')
        },
        data: JSON.stringify(data),
        success: callback
    })
}

function get_data(url, callback) {
    $.ajax({
        type: "GET",
        url: url,
        headers: {
            'X-CSRF-TOKEN': csrftoken
        },
        success: callback,
        error: function (e) {
            console.log(e)
        }
    })
}

function render_researchs(response) {
    let researchs = response.searchs
    let html = ``
    for (let i = 0; i < researchs.length; i++)
        html += `<tr id="tr${researchs[i].id}" data-id="${researchs[i].id}" data-row='${JSON.stringify(researchs[i])}' class="research-table-row cursor-hand-pointer">
                        <td class="td-action">
                             <span class="glyphicon glyphicon-refresh search-refresh"></span>
                        </td>
                        <td class="research-badge"><span class="badge c-bg-blue">2239</span></td>
                        <td class="td-number td-center">${(researchs[i].age) ? researchs[i].age : '-'}</td>
                        <td class="td-date" data-type-id="${researchs[i].type_id ? researchs[i].type_id : null}">${researchs[i].type ? researchs[i].type : '-'}</td>
                        <td class="td-date">${researchs[i].pickup_date ? researchs[i].pickup_date : '-'}</td>
                        <td class="td-number">${researchs[i].dh_o ? researchs[i].dh_o : '-'}</td>
                        <td class="td-place">${researchs[i].origin ? researchs[i].origin : '-'}</td>
                        <td class="td-place">${researchs[i].destination ? researchs[i].destination : '-'}</td>
                        <td class="td-number">${researchs[i].dh_d ? researchs[i].dh_d : '-'}</td>
                        <td class="td-number">${researchs[i].length ? researchs[i].length : '-'}</td>
                        <td class="td-number">${researchs[i].weight ? researchs[i].weight : '-'}</td>
                        <td class="td-action">
                        <span data-id="${researchs[i].id}"  class="glyphicon glyphicon-edit search-edit"></span>
                        <span data-id="${researchs[i].id}" class="glyphicon glyphicon-trash search-remove"></span>
                            </td>
                    </tr>`
    $('#research-table-body').append(html)
}

function render_research_updated(response) {
    let research = response.search
    console.log("research:", research)
    $(`#tr${research.id}`).data('row', research)
    let html = ``
    html += `           <td class="td-action">
                        <span class="glyphicon glyphicon-refresh search-refresh"></span>
                            </td>
                        <td class="research-badge"><span class="badge c-bg-blue">2239</span></td>
                        <td class="td-number td-center">${(research.age) ? research.age : '-'}</td>
                        <td class="td-date" data-type-id="${research.type_id ? research.type_id : null}">${research.type ? research.type : '-'}</td>
                        <td class="td-date">${(research.pickup_date) ? research.pickup_date : '-'}</td>
                        <td class="td-number">${(research.dh_o) ? research.dh_o : '-'}</td>
                        <td class="td-place">${(research.origin) ? research.origin : '-'}</td>
                        <td class="td-place">${(research.destination) ? research.destination : '-'}</td>
                        <td class="td-number">${(research.dh_d) ? research.dh_d : '-'}</td>
                        <td class="td-number">${(research.length) ? research.length : '-'}</td>
                        <td class="td-number">${(research.weight) ? research.weight : '-'}</td>
                        <td class="td-action">  
                        <span data-id="${research.id}" class="glyphicon glyphicon-edit search-edit"></span>
                        <span data-id="${research.id}" class="glyphicon glyphicon-trash search-remove"></span>
                            </td>
                    `
    $(`#tr${research.id}`).html(html)
    console.log(`#tr${research.id}`, JSON.stringify(research))
    $(`#tr${research.id}`).attr('data-row', JSON.stringify(research))
}

function render_research(response) {
    let research = response.search
    console.log("research:", research)
    let html = ``
    html += `<tr id="tr${research.id}" data-id="${research.id}"   data-row='${JSON.stringify(research)}' class="research-table-row cursor-hand-pointer">
                        <td class="td-action">
                        <span class="glyphicon glyphicon-refresh search-refresh"></span>
                            </td>
                        <td class="research-badge"><span class="badge c-bg-blue">2239</span></td>
                        <td class="td-number td-center">${(research.age) ? research.age : '-'}</td>
                        <td class="td-date" data-type-id="${research.type_id ? research.type_id : null}">${research.type ? research.type : '-'}</td>
                        <td class="td-date">${(research.pickup_date) ? research.pickup_date : '-'}</td>
                        <td class="td-number">${(research.dh_o) ? research.dh_o : '-'}</td>
                        <td class="td-place">${(research.origin) ? research.origin : '-'}</td>
                        <td class="td-place">${(research.destination) ? research.destination : '-'}</td>
                        <td class="td-number">${(research.dh_d) ? research.dh_d : '-'}</td>
                        <td class="td-number">${(research.length) ? research.length : '-'}</td>
                        <td class="td-number">${(research.weight) ? research.weight : '-'}</td>
                        <td class="td-action">  
                        <span data-id="${research.id}" class="glyphicon glyphicon-edit search-edit"></span>
                        <span data-id="${research.id}" class="glyphicon glyphicon-trash search-remove"></span>
                            </td>
                    </tr>`
    $('#research-table-body').prepend(html)
    $(`#tr${research.id}`).click()
}

function render_loads(response) {
    let loads = response.loads
    let html = ``
    for (let i = 0; i < loads.length; i++)
        html += `<tr class="result-table-row accordion-toggle collapsed cursor-hand-pointer" data-row='${JSON.stringify(loads[i])}' id="accordion${loads[i].id}"  id="accordion${loads[i].id}" data-toggle="collapse"
                        data-parent="#accordion${loads[i].id}" href="#collapse${loads[i].id}">
                        <td class="td-action">
                             <span data-id="${loads[i].id}" class="renew glyphicon glyphicon-refresh search-refresh"></span>
                        </td>
                        <td class="td-action expand-button">${loads[i].age ? loads[i].age : '-'}</td>
                        <td class="td-date">${loads[i].pickup_date ? loads[i].pickup_date : '-'}</td>
                        <td class="td-date" data-type-id="${loads[i].type_id ? loads[i].type_id : null}">${loads[i].type ? loads[i].type : '-'}</td>
                        <td class="place-column">${loads[i].origin ? loads[i].origin : '-'}</td>
<!--                        <td class="td-number">${loads[i].dh_o ? loads[i].dh_o : '-'}</td>-->
                        <td class="td-number">${loads[i].distance ? loads[i].distance : '-'}</td>
                        <td class="place-column">${loads[i].destination ? loads[i].destination : '-'}</td>
<!--                        // <td class="td-number">${loads[i].dh_d ? loads[i].dh_d : '-'}</td>-->
                        <td class="info-column restrict-text" style="padding-top: 6px; height: 27px;" ><span>${loads[i].name ? loads[i].name : '-'}</span></td>
                        <td class="info-column "><div class="restrict-text">${render_contact_by_type(loads[i].contact_type, loads[i].contact)}</div></td>
                        <td class="td-number">${loads[i].price_render ? loads[i].price_render : '-'}</td>
<!--                        <td class="td-verified"><span class="glyphicon glyphicon-ok verified-icon"></span></td>-->
                        <td class="td-verified">${loads[i].owner_status ? '<span class="glyphicon glyphicon-ok verified-icon"></span>' : ''}</td>
                        <td class="number-column td-action">
                            <span data-id="${loads[i].id}" class="glyphicon glyphicon-edit load-edit"></span>
                            <span data-id="${loads[i].id}" class="glyphicon glyphicon-trash load-remove"></span>
                        </td>
                    </tr>
                    <tr class="hide-table-padding" id="collaps${loads[i].id}"  data-id="collaps${loads[i].id}">
                        <td colspan="11" >
                            <div id="collapse${loads[i].id}" class="collapse p-3" style="text-align: -webkit-center;">
                            <div style="padding: 15px">
                                <div class="row" style="text-align: left;width: 60%">
                                    <div class="col-md-6">
                                        <div class="row">
                                            <div class="col-md-3">
                                                Length:
                                            </div>
                                            <div class="col-md-9">
                                                ${check_data(loads[i].length)}
                                            </div>
                                        </div><br>
                                        <div class="row">
                                            <div class="col-md-3">
                                                Weight:
                                            </div>
                                            <div class="col-md-9">
                                                ${check_data(loads[i].weight)}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6" style="text-align: left">
                                        <div class="row">
                                            <div class="col-md-3">
                                                Description:
                                            </div>
                                            <div class="col-md-9">
                                                ${check_data(loads[i].comment)}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            </div>
                        </td>
                    </tr>`
    $('#load-table-body').append(html)
}

function render_result_loads(response) {
    let loads = response.loads
    let html = ``
    if (loads.length === 0) {
        $('#load-result-table-body').html(`
        <div >
        <div class="no-result">
          <h1>No Result Found</h1>
        </div>
        </div>
        `)
        return
    }
    $('#results-count').html(`${loads.length} results`)
    console.log(loads)
    $('#load-result-table-body').html('')
    for (let i = 0; i < loads.length; i++)
        // console.log(typeof loads[i].dh_o === 'number', loads[i].dh_o)
        html += `<tr class="result-table-row accordion-toggle collapsed cursor-hand-pointer" id="accordion${loads[i].id}" data-id="accordion${loads[i].id}" data-toggle="collapse"
                        data-parent="#accordion${loads[i].id}" href="#collapse${loads[i].id}">
                        <td class="td-action expand-button">${loads[i].age ? loads[i].age : '-'}</td>
                        <td class="td-date">${loads[i].pickup_date ? loads[i].pickup_date : '-'}</td>
                        <td class="td-date" data-type-id="${loads[i].type_id ? loads[i].type_id : null}">${loads[i].type ? loads[i].type : '-'}</td>
                        <td class="td-number">${loads[i].dh_o}</td>
                        <td class="place-column">${loads[i].origin ? loads[i].origin : '-'}</td>
                        <td class="td-number">${loads[i].distance ? loads[i].distance : '-'}</td>
                        <td class="place-column">${loads[i].destination ? loads[i].destination : '-'}</td>
                        <td class="td-number">${loads[i].dh_d}</td>
                        <td class="info-column restrict-text" style="padding-top: 6px; height: 27px;" ><span>${loads[i].name ? loads[i].name : '-'}</span></td>
                        <td class="info-column "><div class="restrict-text">${render_contact_by_type(loads[i].contact_type, loads[i].contact)}</div></td>
                        <td class="td-number">${loads[i].price_render ? loads[i].price_render : '-'}</td>
                        <td class="td-verified">${loads[i].owner_status ? '<span class="glyphicon glyphicon-ok verified-icon"></span>' : ''}</td>
                    </tr>
                 <tr class="hide-table-padding" id="collaps${loads[i].id}" data-id="collaps${loads[i].id}"  >
                        <td colspan="12" >
                            <div id="collapse${loads[i].id}" class="collapse p-3" style="text-align: -webkit-center;">
                            <div style="padding: 15px">
                                <div class="row" style="text-align: left;width: 80%">
                                    <div class="col-md-4" style="text-align: left">
                                        <div class="row">
                                            <div class="col-md-3 div-right">
                                                Ref:
                                            </div>
                                            <div class="col-md-9 div-left">
                                                ${check_data(loads[i].ref_number)}
                                            </div>
                                        </div><br>
                                        <div class="row">
                                            <div class="col-md-3 div-right">
                                                Description:
                                            </div>
                                            <div class="col-md-9 div-left">
                                                ${check_data(loads[i].comment)}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="row">
                                            <div class="col-md-3">
                                                Length:
                                            </div>
                                            <div class="col-md-9">
                                                ${check_data(loads[i].length)}
                                            </div>
                                        </div><br>
                                        <div class="row">
                                            <div class="col-md-3">
                                                Weight:
                                            </div>
                                            <div class="col-md-9">
                                                ${check_data(loads[i].weight)}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                                <div>
                                                    <div class="row">
                                                        <div class="col-md-8 div-right">
                                                            Comp/User ID:
                                                        </div>
                                                        <div class="col-md-3 div-left">
                                                            ${loads[i].customer_id}
                                                        </div>
                                                    </div>
                                                    <br>
                                                    <div class="row">
                                                        <div class="col-md-8 div-right">
                                                            <button onclick="open_comment_modal('${loads[i].owner}')">
                                                                Comments and Review
                                                            </button>
                                                        </div>
                                                        <div class="col-md-4 div-left">

                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                </div>
                            </div>
                            </div>
                        </td>
                    </tr>`
    $('#load-result-table-body').append(html)
}

function render_load(response) {
    let load = response.load
    console.log(response.load)
    let html = ``
    html += `<tr class="result-table-row accordion-toggle accordion-toggle-row collapsed cursor-hand-pointer" data-row='${JSON.stringify(load)}' id="accordion${load.id}"  data-id="accordion${load.id}" data-toggle="collapse"
                        data-parent="#accordion${load.id}" href="#collapse${load.id}">
                        <td class="td-action">
                             <span data-id="${load.id}" class="renew glyphicon glyphicon-refresh search-refresh"></span>
                        </td>
                        <td class="td-action expand-button">${load.age ? load.age : '-'}</td>
                        <td class="td-date">${load.pickup_date ? load.pickup_date : '-'}</td>
                        <td class="td-date" data-type-id="${load.type_id ? load.type_id : null}">${load.type ? load.type : '-'}</td>
                        <td class="place-column">${load.origin ? load.origin : '-'}</td>
<!--                        <td class="td-number">${load.dh_o ? load.dh_o : '-'}</td>-->
                        <td class="td-number">${load.distance ? load.distance : '-'}</td>
                        <td class="place-column">${load.destination ? load.destination : '-'}</td>
<!--                        <td class="place-column">${load.dh_d ? load.dh_d : '-'}</td>-->
                        <td class="info-column restrict-text" style="padding-top: 6px; height: 27px;" ><span>${load.name ? load.name : '-'}</span></td>
                        <td class="info-column "><div class="restrict-text">${render_contact_by_type(load.contact_type, load.contact)}</div></td>
                        <td class="td-number">${load.price_render ? load.price_render : '-'}</td>
                        <td class="td-verified">${load.owner_status ? '<span class="glyphicon glyphicon-ok verified-icon"></span>' : ''}</td>
                        <td class="number-column td-action">
                            <span data-id="${load.id}" class="glyphicon glyphicon-edit load-edit"></span>
                            <span data-id="${load.id}" class="glyphicon glyphicon-trash load-remove"></span>
                        </td>
                    </tr>
                    <tr class="hide-table-padding" id="collaps${load.id}" data-id="collaps${load.id}" >
                        <td colspan="11" >
                            <div id="collapse${load.id}" class="collapse p-3" style="text-align: -webkit-center;">
                            <div style="padding: 15px">
                                <div class="row" style="text-align: left;width: 60%">
                                    <div class="col-md-6">
                                        <div class="row">
                                            <div class="col-md-3">
                                                Length:
                                            </div>
                                            <div class="col-md-9">
                                                ${check_data(load.length)}
                                            </div>
                                        </div><br>
                                        <div class="row">
                                            <div class="col-md-3">
                                                Weight:
                                            </div>
                                            <div class="col-md-9">
                                                ${check_data(load.weight)}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6" style="text-align: left">
                                        <div class="row">
                                            <div class="col-md-3">
                                                Description:
                                            </div>
                                            <div class="col-md-9">
                                                ${check_data(load.comment)}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            </div>
                        </td>
                    </tr>`
    $('#load-table-body').prepend(html)
}

function render_load_updated(response) {
    let load = response.load
    console.log(response.load)
    let html = ``
    $(`#accordion${load.id}`).data('row', load)
    $(`#accordion${load.id}`).html(`
                <td class="td-action">
                             <span data-id="${load.id}" class="renew glyphicon glyphicon-refresh search-refresh"></span>
                        </td>
                <td class="td-action expand-button">${load.age ? load.age : '-'}</td>
                <td class="td-date">${load.pickup_date ? load.pickup_date : '-'}</td>
                <td class="td-date" data-type-id="${load.type_id ? load.type_id : null}">${load.type ? load.type : '-'}</td>
                <td class="place-column">${load.origin ? load.origin : '-'}</td>
<!--                <td class="td-number">${load.dh_o ? load.dh_o : '-'}</td>-->
                <td class="td-number">${load.distance ? load.distance : '-'}</td>
                <td class="place-column">${load.destination ? load.destination : '-'}</td>
<!--                <td class="place-column">${load.dh_d ? load.dh_d : '-'}</td>-->
                <td class="info-column restrict-text" style="padding-top: 6px; height: 27px;" ><span>${load.name ? load.name : '-'}</span></td>
                <td class="info-column "><div class="restrict-text">${render_contact_by_type(load.contact_type, load.contact)}</div></td>
                <td class="td-number">${load.price_render ? load.price_render : '-'}</td>
                <td class="td-verified">${load.owner_status ? '<span class="glyphicon glyphicon-ok verified-icon"></span>' : ''}</td>
                <td class="number-column td-action">
                    <span data-id="${load.id}" class="glyphicon glyphicon-edit load-edit"></span>
                    <span data-id="${load.id}" class="glyphicon glyphicon-trash load-remove"></span>
                </td>
            </tr>`)
    $(`#collaps${load.id}`).html(`
                        <td colspan="11" >
                            <div id="collapse${load.id}" class="collapse p-3" style="text-align: -webkit-center;">
                            <div style="padding: 15px">
                                <div class="row" style="text-align: left;width: 60%">
                                    <div class="col-md-6">
                                        <div class="row">
                                            <div class="col-md-3">
                                                Length:
                                            </div>
                                            <div class="col-md-9">
                                                ${check_data(load.length)}
                                            </div>
                                        </div><br>
                                        <div class="row">
                                            <div class="col-md-3">
                                                Weight:
                                            </div>
                                            <div class="col-md-9">
                                                ${check_data(load.weight)}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6" style="text-align: left">
                                        <div class="row">
                                            <div class="col-md-3">
                                                Description:
                                            </div>
                                            <div class="col-md-9">
                                                ${check_data(load.comment)}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            </div>
                        </td>`)
    // $(`#accordion${load.id}`).html(html)
}

function get_my_research(response = null) {
    if (response)
        console.log(response)
    get_data('/my-researchs/', render_researchs)
}

function get_loads(response = null) {
    if (response)
        console.log(response)
    get_data('/loads/', render_loads)
}