const RIGHTS = [
  { title: "No Harassment", desc: "Lenders and recovery agents cannot use threats, abusive language, or intimidation." },
  { title: "Right to Notice", desc: "You must be given proper written notice before any recovery action is taken." },
  { title: "Fair Recovery Practices", desc: "Recovery must follow RBI/regulatory fair practice guidelines at all times." },
  { title: "Reasonable Call Timing", desc: "Recovery calls should only happen within reasonable hours (typically 7 AM–7 PM)." },
  { title: "Grievance Redressal", desc: "You have the right to file a complaint with the lender's grievance officer." },
  { title: "Written Settlement", desc: "Any settlement agreed upon should be documented and confirmed in writing." },
  { title: "Property Protection", desc: "Recovery agents cannot forcibly seize property without due legal process." },
  { title: "Privacy Rights", desc: "Your personal and financial information must be handled confidentially." },
];

export default function KnowYourRights() {
  return (
    <div>
      <h1 className="page-title">Know Your Rights</h1>
      <p className="page-subtitle">You have rights as a borrower — understand them before negotiating</p>

      <div className="card-grid">
        {RIGHTS.map((r) => (
          <div className="card" key={r.title}>
            <h4 style={{ marginBottom: 8 }}>{r.title}</h4>
            <p style={{ fontSize: 13, color: "var(--text-secondary)" }}>{r.desc}</p>
          </div>
        ))}
      </div>

      <div className="card">
        <h3 style={{ marginBottom: 10 }}>Before You Negotiate</h3>
        <p style={{ fontSize: 14, color: "var(--text-secondary)", lineHeight: 1.6 }}>
          Always keep records of every communication with your lender or recovery agent.
          Request confirmations in writing, understand the total outstanding amount clearly,
          and never make payments without a proper settlement letter or receipt.
        </p>
      </div>
    </div>
  );
}
