# Data contract

`public/data/atlas.json` is generated from the reviewed arrays in `research/`.

| Field | Meaning |
| --- | --- |
| `id` | Stable unique record ID |
| `source`, `target` | Company IDs. Payer to recipient for documented financial flows; otherwise participants, with the exact meaning in `direction_he`. |
| `type` | `investment`, `compute`, `partnership`, `supply`, `acquisition`, `financing` |
| `announced_at` | ISO announcement date, or the described disclosure/update date. `YYYY-MM` is allowed when day is unknown. |
| `date_basis_he` | Optional explanation when a date is a disclosure rather than initial signing. |
| `status` | `announced`, `signed`, `completed`, `proposed`, `reported`, `terminated` |
| `title_he`, `summary_he` | Original Hebrew paraphrases grounded in sources |
| `value.amount` | Numeric native-currency units, not billions. Null if unknown. |
| `value.currency` | `USD`, `EUR`, `GBP`, or null |
| `value.qualifier_he` | Whether the number is cumulative, conditional, an upper bound, share value, etc. |
| `capacity_he` | Optional capacity; distinguish planned from operating capacity. |
| `direction_he` | What the arrow means, including cases with no known payment. |
| `caveat_he` | Conditions, overlap, unresolved closing status and interpretation limits. |
| `sources` | Nonempty array of HTTPS URL, title, publisher, publication date and primary/secondary kind. |
| `verified_at` | Date of research review, not an automatic live status check. |
| `indirect` | Economic relationship through a joint venture, fund or SPV; not direct equity by implication. |
| `historical`, `default_visible`, `superseded_by` | Preserve old events without presenting them as current incremental obligations. |

An aggregate round amount is not a participant's investment. An option is not an exercised investment. Announced compute capacity is not proof it has been delivered. Cancellation rights and financing contingencies belong in the card. Preserve facts at the precision of the source.
