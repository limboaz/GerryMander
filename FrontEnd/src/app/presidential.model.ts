export enum PARTY {
  DEMOCRATS, REPUBLICANS
}

export enum ElectionType {
  CONGRESSIONAL, PRESIDENTIAL
}

export class Candidate {
  constructor(candidate) {
    this.voteTotal = candidate.VoteTotal;
    this.party = (candidate.CandidateParty === 'DEM') ? PARTY.DEMOCRATS : PARTY.REPUBLICANS;
    this.pollingPlaceVotes = candidate.PollingPlaceVotes;
    this.otherVotes = candidate.OtherVotes;
    this.provisionalVotes = candidate.ProvisionalVotes;
    this.earlyVotes = candidate.earlyVotes;
    this.name = candidate.ChoiceName;
  }

  name: string;
  voteTotal: number;
  earlyVotes: number;
  pollingPlaceVotes: number;
  provisionalVotes: number;
  otherVotes: number;
  party: PARTY;
}

export class ElectionData {
  uid: string;
  candidates: Candidate[];
  type: ElectionType;
  year: number;

  constructor(candidates, type, year, uid) {
    this.type = ('presidential' === type) ? ElectionType.PRESIDENTIAL : ElectionType.CONGRESSIONAL;
    this.candidates = candidates;
    this.year = year;
    this.uid = uid;
  }

  setData(uid, candidates) {
    this.uid = uid;
    this.candidates = candidates;
  }
}
