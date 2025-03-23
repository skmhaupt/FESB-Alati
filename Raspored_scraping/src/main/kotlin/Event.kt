import java.time.LocalDateTime

data class Event(
    val id: String,
    val name: String,
    val shortName: String,
    val colorId: Int = 0,
    val professor: String = "",
    val eventType: TimetableType = TimetableType.OTHER,
    val groups: String = "",
    val classroom: String = "",
    val start: LocalDateTime,
    val end: LocalDateTime,
    val description: String? = null,
    val recurring: Boolean = false,
    val recurringType: Recurring = Recurring.UNDEFINED,
    val recurringUntil: String = "",
    val studyCode: String = "",
) {
    fun toCSV(): String {
        return listOf(
            id,
            name,
            shortName,
            colorId,
            professor,
            eventType,
            groups,
            classroom,
            start,
            end,
            description,
            recurring,
            recurringType,
            recurringUntil,
            studyCode
        ).joinToString(",") { it.toString().replace(",", "") }
    }

    fun toCSVHeader(): String {
        return "id, name, shortName, colorId, professor, eventType, groups, classroom, start, end, description, recurring, recurringType, recurringUntil, studyCode"
    }

    override fun toString(): String {
        return "Event(start=${start.toLocalTime()}, end=${end.toLocalTime()})"
    }
}

enum class Recurring {
    ONCE, WEEKLY, EVERY_TWO_WEEKS, MONTHLY, UNDEFINED
}

enum class TimetableType(val value: String) {
    PREDAVANJE("Predavanja"),
    AUDITORNA_VJEZBA("Auditorne vježbe"),
    KOLOKVIJ("Kolokviji"),
    LABORATORIJSKA_VJEZBA("Laboratorijske vježbe"),
    KONSTRUKCIJSKA_VJEZBA("Konstrukcijske vježbe"),
    SEMINAR("Seminari"),
    ISPIT("Ispiti"),
    OTHER("Other")
}