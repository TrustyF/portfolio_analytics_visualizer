export function parse_seconds(time) {
    const hours = Math.floor(time / 3600);
    const minutes = Math.floor((time % 3600) / 60);
    const secs = time % 60;

    const s_hours = String(hours).padStart(2, '0')
    const s_min = String(minutes).padStart(2, '0')
    const s_sec = String(secs).padStart(2, '0')

    if (hours > 0) return `${s_hours}h ${s_min}m`;
    if (minutes > 0) return `${s_min}m ${s_sec}s`;
    return `${s_sec}s`;
}
