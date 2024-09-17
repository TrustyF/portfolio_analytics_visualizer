export function parse_seconds(time) {
    let min = Math.floor(time / 60);
    let sec = time % 60;

    if (min > 10) return '+10'

    return String(min) + ':' + String(sec).padStart(2, '0');
}
