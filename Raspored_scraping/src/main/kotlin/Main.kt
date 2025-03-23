import okhttp3.OkHttpClient
import java.io.File
import java.time.DayOfWeek
import java.time.LocalDate
import java.time.LocalTime
import java.time.format.DateTimeFormatter

suspend fun main() {
    val userNames = readUsernamesFromFile("data/usernames.txt")
    if (userNames.isEmpty()) {
        println("usernames.txt should contain at least 1 username")
        return
    }

    val dates = readUsernamesFromFile("data/dates.txt")
    if (dates.size != 2) {
        println("dates.txt should contain exactly 2 dates")
        return
    }
    val startDate = LocalDate.parse(dates[0], DateTimeFormatter.ofPattern("dd-MM-yyyy"))
    val endDate = LocalDate.parse(dates[1], DateTimeFormatter.ofPattern("dd-MM-yyyy"))

    if (startDate >= endDate) {
        println("Start date must be before end date")
        return
    }

    val times = readUsernamesFromFile("data/times.txt")
    if (dates.size != 2) {
        println("times.txt should contain exactly 2 times")
        return
    }
    val startTime = LocalTime.parse(times[0], DateTimeFormatter.ofPattern("HH:mm"))
    val endTime = LocalTime.parse(times[1], DateTimeFormatter.ofPattern("HH:mm"))
    if (startTime >= endTime) {
        println("Start time must be before end time")
        return
    }

    print("Fetching timetables for ${userNames.size} users from ${startDate.toStringCustom()} to ${endDate.toStringCustom()}\n")
    println("For each user, a CSV file will be created in the data/timetables directory.")
    println("The bigger time range, the longer it will take to fetch the data for each user.\n")

    val timetableService = TimetableService(OkHttpClient())
    val timeTableRepository = TimeTableRepository(timetableService)

    val allEvents = userNames.map { userName ->
        try {
            val events = timeTableRepository.fetchTimetable(userName, startDate, endDate)
            saveToCsv(userName, events, startDate.toStringCustom(), endDate.toStringCustom())
            print("Fetching $userName's timetable completed\n")
            events
        } catch (e: Exception) {
            print("Error fetching timetable for $userName: ${e.message}\n")
            emptyList<Event>()
        }
    }

    val periods = mergePeriods(allEvents)
    saveTimesToCsv(filename = "occupiedTimes", periods)
    val freeTimes = flipPeriods(periods, startTime, endTime)
    saveTimesToCsv(filename = "freeTimes", freeTimes)
    println("Free times saved to data/freeTimes.csv")
}

fun mergePeriods(allEvents: List<List<Event>>): Map<DayOfWeek, MutableList<PeriodTime>> {

    return allEvents.flatten().groupBy { it.start.dayOfWeek }.toSortedMap().map { (day, per) ->
        val events = per.map { event -> PeriodTime(event.start.toLocalTime(), event.end.toLocalTime()) }.distinct()
            .sortedBy { it.end }.sortedBy { it.start }

        val mergedPeriods = mutableListOf(PeriodTime(events.first().start, events.first().end))
        var lastPeriod: PeriodTime = mergedPeriods.last()

        for (i in 1 until events.size) {
            if (!events[i].overlapsWith(lastPeriod)) {
                mergedPeriods.add(PeriodTime(events[i].start, events[i].end))
                lastPeriod = mergedPeriods.lastOrNull() ?: continue
            }
            for (j in i until events.size) {
                if (events[j].overlapsWith(lastPeriod) && lastPeriod.end < events[j].end)
                    lastPeriod.end = events[j].end
                else break
            }
        }
        return@map day to mergedPeriods
    }.toMap()
}

fun flipPeriods(
    wholeWeekPeriods: Map<DayOfWeek, MutableList<PeriodTime>>, startTime: LocalTime, end: LocalTime
): Map<DayOfWeek, MutableList<PeriodTime>> {

    return wholeWeekPeriods.map { (day, periods) ->
        val freeTimes = mutableListOf<PeriodTime>()
        var start = startTime
        periods.forEach {
            if (it.start > start) {
                freeTimes.add(PeriodTime(start, it.start))
            }
            start = it.end
        }
        if (start < end) {
            freeTimes.add(PeriodTime(start, end))
        }
        return@map day to freeTimes
    }.toMap()
}

fun readUsernamesFromFile(filename: String): List<String> {
    return File(filename).readLines().filter { it.isNotBlank() }.filter { !it.startsWith("#") }
}

fun LocalDate.toStringCustom(): String {
    return this.format(DateTimeFormatter.ofPattern("dd-MM-yyyy"))
}

fun saveToCsv(userName: String, events: List<Event>, startDate: String, endDate: String) {
    if (File("data/timetables").mkdirs()) {
        print("Directory data created\n")
    }
    val file = File("data/timetables/${userName}_${startDate}_to_${endDate}.csv")
    file.printWriter().use { out ->
        out.println(events.first().toCSVHeader())
        events.forEach { event ->
            out.print(event.toCSV() + "\r\n")
        }
    }
}

fun saveTimesToCsv(filename: String, freeTimes: Map<DayOfWeek, MutableList<PeriodTime>>) {
    if (File("data/freeTimes").mkdirs()) {
        print("Directory data created\n")
    }
    val file = File("data/freeTimes/$filename.csv")
    file.printWriter().use { out ->
        out.println("DayOfWeek,StartTime,EndTime")
        freeTimes.forEach { (day, periods) ->
            periods.forEach { period ->
                out.print("$day,${period.start},${period.end}\r\n")
            }
        }
    }
}