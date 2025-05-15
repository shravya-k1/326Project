
def run():
    # Get current date
    currentDate = Date.new()
    currentYear = currentDate.getFullYear()
    currentMonth = currentDate.getMonth()

    # DOM elements
    calendarEl = document.getElementById('calendar')
    currentMonthEl = document.getElementById('currentMonth')
    prevMonthBtn = document.getElementById('prevMonth')
    nextMonthBtn = document.getElementById('nextMonth')
    mealFormEl = document.getElementById('mealForm')
    selectedDateEl = document.getElementById('selectedDate')
    saveMealBtn = document.getElementById('saveMeal')
    cancelMealBtn = document.getElementById('cancelMeal')
    mealTypeEl = document.getElementById('mealType')
    mealNameEl = document.getElementById('mealName')
    weekViewEl = document.getElementById('weekView')

    # Load saved meals from DailyDish page
    savedMeals = {}
    try:
        savedMeals = JSON.parse(localStorage.getItem('savedMeals')) or {
            'breakfast': [],
            'lunch': [],
            'dinner': [],
            'snacks': [],
            'dessert': []
        }
        
        # If savedMeals exists but doesn't have all meal types, initialize them
        if not savedMeals.get('breakfast'): savedMeals['breakfast'] = []
        if not savedMeals.get('lunch'): savedMeals['lunch'] = []
        if not savedMeals.get('dinner'): savedMeals['dinner'] = []
        if not savedMeals.get('snacks'): savedMeals['snacks'] = []
        if not savedMeals.get('dessert'): savedMeals['dessert'] = []
    except Exception as e:
        print(f"Error loading saved meals: {e}")
        savedMeals = {
            'breakfast': [],
            'lunch': [],
            'dinner': [],
            'snacks': [],
            'dessert': []
        }

    # Store planned meals
    plannedMeals = JSON.parse(localStorage.getItem('plannedMeals')) or {}

    # Initialize calendar
    renderCalendar(currentYear, currentMonth)
    renderWeekView()

    # Event listeners
    def prev_month(event):
        nonlocal currentMonth, currentYear
        currentMonth -= 1
        if currentMonth < 0:
            currentMonth = 11
            currentYear -= 1
        renderCalendar(currentYear, currentMonth)
    
    def next_month(event):
        nonlocal currentMonth, currentYear
        currentMonth += 1
        if currentMonth > 11:
            currentMonth = 0
            currentYear += 1
        renderCalendar(currentYear, currentMonth)
    
    def cancel_meal(event):
        mealFormEl.style.display = 'none'
    
    def meal_type_change(event):
        updateMealOptions(mealTypeEl.value)
    
    def save_meal(event):
        if not selectedDate:
            return
        
        mealType = mealTypeEl.value
        mealName = mealNameEl.value
        
        if not mealName:
            return
        
        dateKey = formatDateKey(selectedDate)
        
        if not plannedMeals.get(dateKey):
            plannedMeals[dateKey] = []
        
        # Check if this meal type already exists for this date
        existingIndex = -1
        for i, meal in enumerate(plannedMeals[dateKey]):
            if meal['type'] == mealType:
                existingIndex = i
                break
        
        if existingIndex >= 0:
            # Replace existing meal of this type
            plannedMeals[dateKey][existingIndex] = {
                'type': mealType,
                'name': mealName
            }
        else:
            # Add new meal
            plannedMeals[dateKey].append({
                'type': mealType,
                'name': mealName
            })
        
        localStorage.setItem('plannedMeals', JSON.stringify(plannedMeals))
        renderCalendar(currentYear, currentMonth)
        renderWeekView()
        mealFormEl.style.display = 'none'

    prevMonthBtn.addEventListener('click', create_proxy(prev_month))
    nextMonthBtn.addEventListener('click', create_proxy(next_month))
    cancelMealBtn.addEventListener('click', create_proxy(cancel_meal))
    mealTypeEl.addEventListener('change', create_proxy(meal_type_change))
    saveMealBtn.addEventListener('click', create_proxy(save_meal))

    # Update meal options based on selected type
    def updateMealOptions(mealType):
        mealNameEl.innerHTML = ''
        
        # Add default option
        defaultOption = document.createElement('option')
        defaultOption.value = ''
        defaultOption.textContent = '-- Select a meal --'
        mealNameEl.appendChild(defaultOption)
        
        # Add saved meals for this type
        if savedMeals.get(mealType) and len(savedMeals[mealType]) > 0:
            for meal in savedMeals[mealType]:
                option = document.createElement('option')
                option.value = meal['name']
                option.textContent = meal['name']
                mealNameEl.appendChild(option)
        else:
            noMealsOption = document.createElement('option')
            noMealsOption.value = ''
            noMealsOption.textContent = 'No saved meals for this type'
            mealNameEl.appendChild(noMealsOption)

    # Render calendar function
    def renderCalendar(year, month):
        # Update month header
        monthNames = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]
        currentMonthEl.textContent = f"{monthNames[month]} {year}"
        
        # Get first and last day of month
        firstDay = Date.new(year, month, 1)
        lastDay = Date.new(year, month + 1, 0)
        
        # Get days in month
        daysInMonth = lastDay.getDate()
        
        # Get starting day of week (0-6)
        startDay = firstDay.getDay()
        
        # Clear calendar
        calendarEl.innerHTML = ''
        
        # Add day headers
        dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for day in dayNames:
            dayHeader = document.createElement('div')
            dayHeader.className = 'day-header'
            dayHeader.textContent = day
            calendarEl.appendChild(dayHeader)
        
        # Add empty cells for days before the first day of month
        for i in range(startDay):
            emptyDay = document.createElement('div')
            emptyDay.className = 'day empty'
            calendarEl.appendChild(emptyDay)
        
        # Add days of month
        for day in range(1, daysInMonth + 1):
            date = Date.new(year, month, day)
            dateKey = formatDateKey(date)
            dayEl = document.createElement('div')
            dayEl.className = 'day'
            
            # Add day number
            dayNumber = document.createElement('div')
            dayNumber.className = 'day-number'
            dayNumber.textContent = day
            dayEl.appendChild(dayNumber)
            
            # Add meals if any
            if plannedMeals.get(dateKey) and len(plannedMeals[dateKey]) > 0:
                for meal in plannedMeals[dateKey]:
                    mealEl = document.createElement('div')
                    mealEl.className = f"meal-item {meal['type']}"
                    mealEl.innerHTML = f"""
                        {meal['name']}
                        <span class="remove-meal" data-date="{dateKey}" data-type="{meal['type']}">✕</span>
                    """
                    dayEl.appendChild(mealEl)
            
            # Add click event
            def day_click_handler(e, date=date, month=month, day=day, year=year):
                # Don't open form if clicking on remove button
                if e.target.classList.contains('remove-meal'):
                    return
                
                nonlocal selectedDate
                selectedDate = date
                selectedDateEl.textContent = f"{monthNames[month]} {day}, {year}"
                mealFormEl.style.display = 'block'
                
                # Set default meal type and update options
                mealTypeEl.value = 'breakfast'
                updateMealOptions('breakfast')
            
            dayEl.addEventListener('click', create_proxy(day_click_handler))
            
            # Highlight current day
            today = Date.new()
            if (date.getDate() == today.getDate() and 
                date.getMonth() == today.getMonth() and 
                date.getFullYear() == today.getFullYear()):
                dayEl.style.border = '2px solid #4CAF50'
            
            calendarEl.appendChild(dayEl)
        
        # Add event listeners to remove buttons
        for btn in document.querySelectorAll('.remove-meal'):
            def remove_handler(e, btn=btn):
                dateKey = btn.getAttribute('data-date')
                mealType = btn.getAttribute('data-type')
                
                if plannedMeals.get(dateKey):
                    plannedMeals[dateKey] = [meal for meal in plannedMeals[dateKey] if meal['type'] != mealType]
                    
                    if len(plannedMeals[dateKey]) == 0:
                        del plannedMeals[dateKey]
                    
                    localStorage.setItem('plannedMeals', JSON.stringify(plannedMeals))
                    renderCalendar(year, month)
                    renderWeekView()
            
            btn.addEventListener('click', create_proxy(remove_handler))
    
    # Render week view
    def renderWeekView():
        weekViewEl.innerHTML = ''
        
        today = Date.new()
        currentDay = today.getDay() # 0 (Sun) to 6 (Sat)
        startOfWeek = Date.new(today)
        startOfWeek.setDate(today.getDate() - currentDay)
        
        for i in range(7):
            day = Date.new(startOfWeek)
            day.setDate(startOfWeek.getDate() + i)
            dateKey = formatDateKey(day)
            
            dayEl = document.createElement('div')
            dayEl.className = 'week-day'
            
            dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
            dayName = dayNames[i]
            dayNumber = day.getDate()
            monthNamesShort = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            monthName = monthNamesShort[day.getMonth()]
            
            dayEl.innerHTML = f"<h4>{dayName}<br>{monthName} {dayNumber}</h4>"
            
            if plannedMeals.get(dateKey) and len(plannedMeals[dateKey]) > 0:
                for meal in plannedMeals[dateKey]:
                    mealEl = document.createElement('div')
                    mealEl.className = f"meal-item {meal['type']}"
                    mealTypeCapitalized = meal['type'][0].upper() + meal['type'][1:]
                    mealEl.innerHTML = f"""
                        <strong>{mealTypeCapitalized}:</strong> {meal['name']}
                        <span class="remove-meal" data-date="{dateKey}" data-type="{meal['type']}">✕</span>
                    """
                    dayEl.appendChild(mealEl)
            else:
                emptyEl = document.createElement('div')
                emptyEl.className = 'empty-day'
                emptyEl.textContent = 'No meals planned'
                dayEl.appendChild(emptyEl)
            
            weekViewEl.appendChild(dayEl)
    
    # Helper function to format date as key
    def formatDateKey(date):
        return f"{date.getFullYear()}-{date.getMonth()}-{date.getDate()}"

    # Initialize selectedDate
    selectedDate = None

# Run the app when DOM is loaded
document.addEventListener('DOMContentLoaded', create_proxy(run))
