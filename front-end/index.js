const treeContainer = document.getElementById('employee-tree')
const url = 'http://127.0.0.1:5000/get_subordinates'


async function fetchSubordinates(id = null) {
    let fetchUrl = url
    if (id !== null) fetchUrl += `?id=${id}`
    const res = await fetch(fetchUrl)
    return await res.json()
}

async function fetchEmployeeById(id) {
    const res = await fetch(`http://127.0.0.1:5000/get_employee_by_id?id=${id}`)
    return await res.json()
}

function showEmployeeInfo(employee) {
    const infoDiv = document.getElementById('employee-info')
    if (!employee || employee.error) {
        infoDiv.classList.remove('active')
        infoDiv.innerHTML = ''
        return
    }
    infoDiv.innerHTML = `
        <h3>${employee.full_name}</h3>
        <p><b>Должность:</b> ${employee.position}</p>
        <p><b>Дата приёма:</b> ${employee.hire_date}</p>
        <p><b>Зарплата:</b> ${employee.salary} руб.</p>
        <p><b>Начальник:</b> ${employee.boss_name ? employee.boss_name : '—'}</p>
    `
    infoDiv.classList.add('active')
}

let lastSelectedLi = null

function createTreeNode(employee) {
    const li = document.createElement('li')
    // Добавляем имя и должность сотрудника
    li.textContent = `${employee.full_name} (${employee.position})`
    // Добавляем курсор
    li.style.cursor = employee.has_subordinates ? 'pointer' : 'default'
    // Добавляем id сотрудника
    li.dataset.id = employee.id

    // Клик по сотруднику — показать инфо
    li.addEventListener('click', async function (e) {
        e.stopPropagation()
        // Подсветка выбранного
        if (lastSelectedLi) lastSelectedLi.classList.remove('selected')
        li.classList.add('selected')
        lastSelectedLi = li
        // Получить инфо и показать
        const info = await fetchEmployeeById(employee.id)
        showEmployeeInfo(info)
    })

    // Если сотрудник имеет подчинённых, то добавляем класс closed
    if (employee.has_subordinates) {
        // Добавляем класс closed
        li.classList.add('tree-closed')
        // Добавляем обработчик клика
        li.addEventListener('dblclick', function (e) {
            e.stopPropagation()
            if (li.classList.contains('tree-opened')) {
                // Сворачиваем
                const ul = li.querySelector('ul')
                // Удаляем подчинённых из дерева
                if (ul) ul.remove()
                // Убираем класс opened и добавляем класс closed
                li.classList.remove('tree-opened')
                li.classList.add('tree-closed')
            } 
            else {
                // Разворачиваем
                fetchSubordinates(employee.id)
                .then(subs => {
                    const ul = document.createElement('ul')
                    // Добавляем подчинённых в дерево
                    for (const sub of subs) {
                        ul.appendChild(createTreeNode(sub))
                    }
                                        
                    li.appendChild(ul)

                    li.classList.remove('tree-closed')
                    li.classList.add('tree-opened')
                })
            }
        })
    }
    return li
}


async function renderEmployeeTree() {
    const rootEmployees = await fetchSubordinates()
    treeContainer.innerHTML = ''
    const ul = document.createElement('ul')
    for (const emp of rootEmployees) {
        ul.appendChild(createTreeNode(emp))
    }
    treeContainer.appendChild(ul)
}

document.addEventListener('DOMContentLoaded', () => {
    renderEmployeeTree()
})


