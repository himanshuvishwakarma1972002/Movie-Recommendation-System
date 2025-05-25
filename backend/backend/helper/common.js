const n_i_validator=require("node-input-validator")
    
module.exports={
    validators: async function (rules, request) {
		for (const key in rules) {
			if (Object.hasOwnProperty.call(rules, key)) {
				const rule = rules[key];

				if (rule.includes("sometimes")) {
					// If sometimes rule is present
					if (!request[key]) {
						// If the value not present, then skip the rule
						delete rules[key];
					}
				}
			}
		}

		const v = new niv.Validator(request, rules);
		const matched = await v.check();
		if (!matched) {
			return { status: false, errors: v.errors };
		} else {
			return { status: true };
		}
	},
}