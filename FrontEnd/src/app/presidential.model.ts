export class Presidential {
  uid: string;
  candidate: string;
  party: string;
  voteTotal: number;
  constructor() {
  }
  setData(uid, candidate, party, voteTotal) {
    this.uid = uid;
    this.candidate = candidate;
    this.party = party;
    this.voteTotal = voteTotal;
  }
}
