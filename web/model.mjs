export function difference([earlier, later]) {
  return {number: later - earlier, percent: earlier === 0 ? null : (later - earlier) / earlier * 100};
}
