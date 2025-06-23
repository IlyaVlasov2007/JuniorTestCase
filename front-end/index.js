const url = 'http://127.0.0.1:5000/get_employees?page='
let currentPage = 1

function getEmployeesAndCreateCards(page) {
    // Функция получает данные с сервера и создает карточки сотрудников
    fetch(url + page)
        .then(response => response.json())
        .then(data => {
            // Получаем контейнер для карточек сотрудников
            const mainContainer = document.getElementById('employee-container')
            
            // Создаем карточки для каждого сотрудника
            for (const employee of data.employees) {
                const employeeCard = document.createElement('div')
                employeeCard.className = 'employee-card'

                const employeeName = document.createElement('h3')
                employeeName.textContent = employee.full_name

                const employeePosition = document.createElement('p')
                employeePosition.textContent = employee.position

                const employeeDateOfEmployment = document.createElement('p')
                employeeDateOfEmployment.textContent = employee.hire_date        

                const employeeSalary = document.createElement('p')
                employeeSalary.textContent = employee.salary + ' руб.'

                const employeeBoss = document.createElement('p')
                employeeBoss.textContent = employee.boss_name

                employeeCard.appendChild(employeeName)
                employeeCard.appendChild(employeePosition)
                employeeCard.appendChild(employeeDateOfEmployment)
                employeeCard.appendChild(employeeSalary)
                employeeCard.appendChild(employeeBoss)

                mainContainer.appendChild(employeeCard)
            } 
        })
}



document.addEventListener('DOMContentLoaded', () => {
    getEmployeesAndCreateCards(currentPage)

    // AJAX запрос при скролле
    window.addEventListener('scroll', () => {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
            currentPage++
            getEmployeesAndCreateCards(currentPage)
        }
    })
})


