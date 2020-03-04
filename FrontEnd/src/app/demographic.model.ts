export class Demographic {
  uid: string;
  total: number;
  white: number;
  black: number;
  asian: number;
  hawaiian: number;
  others: number;
  hispanic = 0;
  constructor() {
  }
  setData(uid, total, white, black, asian, hawaiian, others) {
    this.uid = uid;
    this.total = total;
    this.white = white;
    this.black = black;
    this.asian = asian;
    this.hawaiian = hawaiian;
    this.others = others;
  }
}
