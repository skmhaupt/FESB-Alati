import java.time.LocalTime

data class PeriodTime(var start: LocalTime, var end: LocalTime)

fun PeriodTime.overlapsWith(other: PeriodTime): Boolean {
    val otherStartsBeforeThisEnds = other.start <= this.end
    val otherEndsAfterThisStarts = other.end >= this.start
    return otherEndsAfterThisStarts && otherStartsBeforeThisEnds
}