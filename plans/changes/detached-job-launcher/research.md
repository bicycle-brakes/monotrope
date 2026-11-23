---
title: "Research — detached-job-launcher"
status: draft
implementation_status: none
date: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-a6ns.1
owner: Data Architect
provenance: ai-drafted-reviewed
neighbours: []
produced_by: {kind: llm-session, name: stage2-research-swarm, version: "2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# detached job launcher — Research

<!-- research-swarm/v2 run 78d86db692f0b3f8ac643375833febff -->

## Research swarm — 2026-11-23

run 78d86db692f0b3f8ac643375833febff · class feature · baseline HEAD 3a330a622be0 · input digest 2c36f3807b1fec28

```research-swarm/v2 manifest
{
  "budget": 42,
  "catalog": {
    "address_notices": [
      "opencode-go/gemini-4-argon: wire api \"google-generative-ai\" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base"
    ],
    "candidates": [
      {
        "detail": "a paid model; the free class does not admit it",
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": false,
              "canonical_model_id": "reflection/beam-1.0-501b-a23b",
              "cost": {
                "cache_read": 0,
                "input": 0,
                "output": 0
              },
              "description": "Sparse mixture-of-experts reasoning model with 23B active parameters for coding and agentic workflows",
              "family": "beam-free",
              "id": "beam-free",
              "interleaved": {
                "field": "reasoning_content"
              },
              "knowledge": "2026-06-30",
              "last_updated": "2026-10-16",
              "limit": {
                "context": 1048576,
                "output": 131072
              },
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Beam Free",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "low",
                    "medium",
                    "high",
                    "xhigh",
                    "max"
                  ]
                }
              ],
              "release_date": "2026-10-05",
              "structured_output": true,
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "beam-free"
          },
          "pi": {
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "beam-free",
        "reason": "paid-admitted"
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "tencent/hy4-flash",
              "cost": {
                "cache_read": 0,
                "input": 0,
                "output": 0
              },
              "description": "Tencent's lower-cost Hy4 tier for everyday agent and productivity tasks, with image understanding and a 1M-token context window.",
              "family": "hy-flash-free",
              "id": "hy4-flash-free",
              "last_updated": "2026-11-16",
              "limit": {
                "context": 1048576,
                "input": 983040,
                "output": 65536
              },
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Hy4 flash Free",
              "open_weights": false,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "none",
                    "high"
                  ]
                }
              ],
              "release_date": "2026-11-16",
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "hy4-flash-free"
          },
          "pi": {
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "hy4-flash-free",
        "reason": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": false,
              "cost": {
                "cache_read": 0,
                "input": 0,
                "output": 0
              },
              "description": "Stealth model, free for a limited time",
              "id": "iceman-contributor-free",
              "last_updated": "2026-10-24",
              "limit": {
                "context": 262144,
                "output": 131072
              },
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Iceman Contributor Free",
              "open_weights": false,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [],
              "release_date": "2026-10-24",
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "iceman-contributor-free"
          },
          "pi": {
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "iceman-contributor-free",
        "reason": "excluded"
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "meituan/longcat-2.5",
              "cost": {
                "cache_read": 0,
                "input": 0,
                "output": 0
              },
              "description": "Meituan's multimodal reasoning model for long-horizon coding and agent tasks, with visual understanding and a 1M-token context window",
              "family": "longcat-free",
              "id": "longcat-2.5-free",
              "interleaved": {
                "field": "reasoning_content"
              },
              "last_updated": "2026-11-02",
              "limit": {
                "context": 1000000,
                "output": 262144
              },
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "LongCat 2.5 Free",
              "open_weights": false,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "toggle"
                }
              ],
              "release_date": "2026-11-02",
              "status": "deprecated",
              "temperature": false,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "longcat-2.5-free"
          },
          "pi": {
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": true,
            "value": "deprecated"
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "longcat-2.5-free",
        "reason": "deprecated"
      }
    ],
    "capability_reason": null,
    "capability_status": "available",
    "measured_wire_apis": [
      "openai-completions",
      "anthropic-messages",
      "openai-responses"
    ],
    "models": [
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "anthropic/claude-haiku-5-5",
              "cost": {
                "cache_read": 0.01,
                "cache_write": 0.125,
                "input": 0.1,
                "output": 0.5,
                "tiers": [
                  {
                    "cache_read": 0.05,
                    "cache_write": 0.625,
                    "input": 0.5,
                    "output": 2.5,
                    "tier": {
                      "size": 100000,
                      "type": "context"
                    }
                  }
                ]
              },
              "description": "Fast Claude model for responsive assistance, classification, and lightweight agents",
              "family": "claude-haiku",
              "id": "claude-haiku-5-5",
              "knowledge": "2026-06",
              "last_updated": "2026-10-07",
              "limit": {
                "context": 1000000,
                "output": 128000
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "pdf"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Claude Haiku 5.5",
              "open_weights": false,
              "provider": {
                "api": "https://opencode.ai/inference/go/anthropic/v1",
                "npm": "@ai-sdk/anthropic"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "toggle"
                },
                {
                  "type": "effort",
                  "values": [
                    "low",
                    "medium",
                    "high",
                    "xhigh",
                    "max"
                  ]
                }
              ],
              "release_date": "2026-10-07",
              "structured_output": true,
              "temperature": false,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "claude-haiku-5-5"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "anthropic-messages"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/anthropic"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "claude-haiku-5-5",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": false,
              "canonical_model_id": "deepseek/deepseek-v4-pro",
              "cost": {
                "cache_read": 0.022,
                "input": 0.66,
                "output": 1.98
              },
              "description": "Flagship DeepSeek model for coding, reasoning, and agentic work",
              "family": "deepseek-pro",
              "id": "deepseek-v4-pro",
              "interleaved": {
                "field": "reasoning_content"
              },
              "knowledge": "2025-05",
              "last_updated": "2026-04-24",
              "limit": {
                "context": 1000000,
                "output": 384000
              },
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "DeepSeek V4 Pro",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "high",
                    "max"
                  ]
                }
              ],
              "release_date": "2026-04-24",
              "structured_output": true,
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "deepseek-v4-pro"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "deepseek-v4-pro",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "deepseek/deepseek-v4.1-flash-1017",
              "cost": {
                "cache_read": 0.003,
                "input": 0.15,
                "output": 0.6
              },
              "description": "October 17 update of DeepSeek V4.1 Flash with improved reasoning, coding, agentic tasks, and visual understanding",
              "family": "deepseek-flash",
              "id": "deepseek-v4.1-flash",
              "interleaved": {
                "field": "reasoning_content"
              },
              "knowledge": "2025-05",
              "last_updated": "2026-10-17",
              "limit": {
                "context": 1000000,
                "output": 384000
              },
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "DeepSeek V4.1 Flash 1017",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "low",
                    "high",
                    "max"
                  ]
                }
              ],
              "release_date": "2026-10-17",
              "structured_output": true,
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "deepseek-v4.1-flash"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "deepseek-v4.1-flash",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "google/gemini-4-argon",
              "cost": {
                "cache_read": 0.1,
                "input": 2,
                "input_audio": 2,
                "output": 10
              },
              "description": "Google's flagship reasoning model for complex software engineering, deep math and science, and long-horizon autonomous agents",
              "family": "gemini",
              "id": "gemini-4-argon",
              "knowledge": "2026-03",
              "last_updated": "2026-10-13",
              "limit": {
                "context": 1048576,
                "output": 65536
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "video",
                  "audio",
                  "pdf"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Gemini 4 Argon",
              "open_weights": false,
              "provider": {
                "api": "https://opencode.ai/inference/go/google/v1beta",
                "npm": "@ai-sdk/google"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "low",
                    "medium",
                    "high"
                  ]
                }
              ],
              "release_date": "2026-10-13",
              "structured_output": true,
              "temperature": false,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "gemini-4-argon"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "google-generative-ai"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/google/v1beta"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "gemini-4-argon",
        "reason": "wire-api-not-measured",
        "tool_support": "not-assessed"
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": false,
              "canonical_model_id": "zhipuai/glm-5.2",
              "cost": {
                "cache_read": 0.26,
                "input": 1.4,
                "output": 4.4
              },
              "description": "Open flagship GLM for long-horizon coding agents and million-token context work",
              "family": "glm",
              "id": "glm-5.2",
              "interleaved": {
                "field": "reasoning_content"
              },
              "last_updated": "2026-06-13",
              "limit": {
                "context": 1000000,
                "output": 131072
              },
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "GLM-5.2",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "high",
                    "max"
                  ]
                }
              ],
              "release_date": "2026-06-13",
              "status": "deprecated",
              "structured_output": true,
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "glm-5.2"
          },
          "pi": {
            "api": {
              "present": false
            },
            "baseUrl": {
              "present": false
            },
            "input": {
              "present": false
            },
            "provider": {
              "present": false
            },
            "type": {
              "present": false
            }
          },
          "status": {
            "present": true,
            "value": "deprecated"
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "glm-5.2",
        "reason": "baseline-only",
        "tool_support": "not-assessed"
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": false,
              "canonical_model_id": "zhipuai/glm-5.3",
              "cost": {
                "cache_read": 0.26,
                "input": 1.4,
                "output": 4.4
              },
              "description": "Flagship GLM model for long-horizon coding, agents, and complex project delivery",
              "family": "glm",
              "id": "glm-5.3",
              "interleaved": {
                "field": "reasoning_content"
              },
              "last_updated": "2026-08-14",
              "limit": {
                "context": 1000000,
                "output": 131072
              },
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "GLM-5.3",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "low",
                    "high",
                    "max"
                  ]
                }
              ],
              "release_date": "2026-08-14",
              "structured_output": true,
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "glm-5.3"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "glm-5.3",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "zhipuai/glm-5.3-flash",
              "cost": {
                "cache_read": 0.03,
                "input": 0.15,
                "output": 0.5
              },
              "description": "Native multimodal GLM model for efficient coding and long-horizon agent tasks",
              "family": "glm-flash",
              "id": "glm-5.3-flash",
              "interleaved": {
                "field": "reasoning_content"
              },
              "last_updated": "2026-08-26",
              "limit": {
                "context": 1000000,
                "output": 131072
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "video"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "GLM-5.3-Flash",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "low",
                    "high",
                    "max"
                  ]
                }
              ],
              "release_date": "2026-08-26",
              "structured_output": true,
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "glm-5.3-flash"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "glm-5.3-flash",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "openai/gpt-5.6-luna",
              "cost": {
                "cache_read": 0.02,
                "cache_write": 0.25,
                "context_over_200k": {
                  "cache_read": 0.04,
                  "cache_write": 0.5,
                  "input": 0.4,
                  "output": 1.8
                },
                "input": 0.2,
                "output": 1.2,
                "tiers": [
                  {
                    "cache_read": 0.04,
                    "cache_write": 0.5,
                    "input": 0.4,
                    "output": 1.8,
                    "tier": {
                      "size": 272000,
                      "type": "context"
                    }
                  }
                ]
              },
              "description": "Cost-efficient GPT-5.6 model for fast, high-volume workloads",
              "family": "gpt-luna",
              "id": "gpt-5.6-luna",
              "knowledge": "2026-02-16",
              "last_updated": "2026-07-09",
              "limit": {
                "context": 1050000,
                "input": 922000,
                "output": 128000
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "pdf"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "GPT-5.6 Luna",
              "open_weights": false,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1",
                "npm": "@ai-sdk/openai"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "none",
                    "low",
                    "medium",
                    "high",
                    "xhigh",
                    "max"
                  ]
                }
              ],
              "release_date": "2026-07-09",
              "structured_output": true,
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "gpt-5.6-luna"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-responses"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "gpt-5.6-luna",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "openai/gpt-6-luna",
              "cost": {
                "cache_read": 0.01,
                "cache_write": 0.125,
                "context_over_200k": {
                  "cache_read": 0.02,
                  "cache_write": 0.25,
                  "input": 0.2,
                  "output": 0.75
                },
                "input": 0.1,
                "output": 0.5,
                "tiers": [
                  {
                    "cache_read": 0.02,
                    "cache_write": 0.25,
                    "input": 0.2,
                    "output": 0.75,
                    "tier": {
                      "size": 272000,
                      "type": "context"
                    }
                  }
                ]
              },
              "description": "OpenAI's most efficient model for focused, high-volume tasks",
              "family": "gpt-luna",
              "id": "gpt-6-luna",
              "knowledge": "2026-05-18",
              "last_updated": "2026-09-22",
              "limit": {
                "context": 1050000,
                "input": 922000,
                "output": 128000
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "pdf"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "GPT-6 Luna",
              "open_weights": false,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1",
                "npm": "@ai-sdk/openai"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "none",
                    "low",
                    "medium",
                    "high",
                    "xhigh",
                    "max"
                  ]
                }
              ],
              "release_date": "2026-09-22",
              "structured_output": true,
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "gpt-6-luna"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-responses"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "gpt-6-luna",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "xai/grok-4.7",
              "cost": {
                "cache_read": 0.5,
                "context_over_200k": {
                  "cache_read": 1,
                  "input": 4,
                  "output": 12
                },
                "input": 2,
                "output": 6,
                "tiers": [
                  {
                    "cache_read": 1,
                    "input": 4,
                    "output": 12,
                    "tier": {
                      "size": 200000,
                      "type": "context"
                    }
                  }
                ]
              },
              "description": "xAI's frontier model for long-running agents, coding, knowledge work, and visual projects",
              "family": "grok",
              "id": "grok-4.7",
              "knowledge": "2026-05",
              "last_updated": "2026-09-21",
              "limit": {
                "context": 500000,
                "output": 500000
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "pdf"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Grok 4.7",
              "open_weights": false,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1",
                "npm": "@ai-sdk/openai"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "low",
                    "medium",
                    "high",
                    "xhigh"
                  ]
                }
              ],
              "release_date": "2026-09-21",
              "structured_output": true,
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "grok-4.7"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-responses"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "grok-4.7",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": false,
              "canonical_model_id": "tencent/hy3",
              "cost": {
                "cache_read": 0.035,
                "input": 0.14,
                "output": 0.58
              },
              "description": "Tencent Hy reasoning model for coding, instruction following, and agent tasks",
              "family": "hy",
              "id": "hy3",
              "last_updated": "2026-07-06",
              "limit": {
                "context": 256000,
                "input": 192000,
                "output": 128000
              },
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Hy3",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "none",
                    "low",
                    "high"
                  ]
                }
              ],
              "release_date": "2026-07-06",
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "hy3"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "hy3",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "tencent/hy4",
              "cost": {
                "cache_read": 0.042,
                "input": 0.834,
                "output": 2.501
              },
              "description": "A next-generation multimodal productivity model with significantly enhanced Agent and complex task execution capabilities.",
              "family": "hy",
              "id": "hy4",
              "last_updated": "2026-11-04",
              "limit": {
                "context": 1048576,
                "input": 983010,
                "output": 65536
              },
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Hy4",
              "open_weights": false,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "none",
                    "high"
                  ]
                }
              ],
              "release_date": "2026-11-04",
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "hy4"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "hy4",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": false,
              "canonical_model_id": "tencent/hy4-preview",
              "cost": {
                "cache_read": 0.042,
                "input": 0.834,
                "output": 2.501
              },
              "description": "A next-generation productivity model with significantly enhanced Agent and complex task execution capabilities.",
              "family": "hy",
              "id": "hy4-preview",
              "last_updated": "2026-08-28",
              "limit": {
                "context": 1024000,
                "output": 64000
              },
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Hy4 preview",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "none",
                    "high"
                  ]
                }
              ],
              "release_date": "2026-08-28",
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "hy4-preview"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "hy4-preview",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "moonshotai/kimi-k2.7-code",
              "cost": {
                "cache_read": 0.19,
                "input": 0.95,
                "output": 4
              },
              "description": "Coding-focused Kimi model, stronger on long-horizon repo work with less overthinking",
              "family": "kimi-code",
              "id": "kimi-k2.7-code",
              "interleaved": {
                "field": "reasoning_content"
              },
              "knowledge": "2025-01",
              "last_updated": "2026-06-12",
              "limit": {
                "context": 262144,
                "output": 262144
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "video"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Kimi K2.7 Code",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [],
              "release_date": "2026-06-12",
              "structured_output": true,
              "temperature": false,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "kimi-k2.7-code"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "kimi-k2.7-code",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "moonshotai/kimi-k3",
              "cost": {
                "cache_read": 0.3,
                "cache_write": 3,
                "input": 3,
                "output": 15
              },
              "description": "Multimodal Kimi model with 1M context and toggleable max-effort thinking for long-horizon agent work",
              "family": "kimi",
              "id": "kimi-k3",
              "interleaved": {
                "field": "reasoning_content"
              },
              "last_updated": "2026-07-16",
              "limit": {
                "context": 1048576,
                "output": 1048576
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "video"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Kimi K3",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "max"
                  ]
                }
              ],
              "release_date": "2026-07-16",
              "structured_output": true,
              "temperature": false,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "kimi-k3"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "kimi-k3",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "moonshotai/kimi-k3.1-pro",
              "cost": {
                "cache_read": 0.2,
                "cache_write": 2,
                "input": 2,
                "output": 10
              },
              "description": "Multimodal Kimi model with a 1M-token context window and always-on reasoning, for coding, 3D creation and financial research",
              "family": "kimi-pro",
              "id": "kimi-k3.1-pro",
              "interleaved": {
                "field": "reasoning_content"
              },
              "last_updated": "2026-10-23",
              "limit": {
                "context": 1048576,
                "output": 1048576
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "video"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Kimi K3.1 Pro",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "low",
                    "high",
                    "max"
                  ]
                }
              ],
              "release_date": "2026-10-23",
              "structured_output": true,
              "temperature": false,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "kimi-k3.1-pro"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "kimi-k3.1-pro",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": false,
              "canonical_model_id": "meituan/longcat-2.0",
              "cost": {
                "cache_read": 0.006,
                "input": 0.3,
                "output": 1.2
              },
              "description": "Meituan LongCat-2.0, a reasoning model with tool calling and a 1M-token context window",
              "family": "longcat",
              "id": "longcat-2.0",
              "interleaved": {
                "field": "reasoning_content"
              },
              "last_updated": "2026-06-30",
              "limit": {
                "context": 1000000,
                "output": 131072
              },
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "LongCat-2.0",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "toggle"
                }
              ],
              "release_date": "2026-06-30",
              "status": "deprecated",
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "longcat-2.0"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": true,
            "value": "deprecated"
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "longcat-2.0",
        "reason": null,
        "tool_support": "deprecated"
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "xiaomi/mimo-v2.5",
              "cost": {
                "cache_read": 0.0028,
                "input": 0.14,
                "output": 0.28
              },
              "description": "MiMo omni model for text, image, video, audio, and agents",
              "family": "mimo",
              "id": "mimo-v2.5",
              "interleaved": {
                "field": "reasoning_content"
              },
              "knowledge": "2024-12",
              "last_updated": "2026-04-22",
              "limit": {
                "context": 1000000,
                "output": 128000
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "audio",
                  "video"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "MiMo V2.5",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [],
              "release_date": "2026-04-22",
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "mimo-v2.5"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "mimo-v2.5",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": false,
              "canonical_model_id": "xiaomi/mimo-v2.5-pro",
              "cost": {
                "cache_read": 0.003625,
                "input": 0.435,
                "output": 0.87
              },
              "description": "MiMo pro model for strong multimodal reasoning and agent execution",
              "family": "mimo-pro",
              "id": "mimo-v2.5-pro",
              "interleaved": {
                "field": "reasoning_content"
              },
              "knowledge": "2024-12",
              "last_updated": "2026-04-22",
              "limit": {
                "context": 1048576,
                "output": 128000
              },
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "MiMo V2.5 Pro",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [],
              "release_date": "2026-04-22",
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "mimo-v2.5-pro"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "mimo-v2.5-pro",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "xiaomi/mimo-v2.6-flash",
              "cost": {
                "cache_read": 0.0028,
                "input": 0.14,
                "output": 0.28
              },
              "description": "MiMo Flash model for multimodal coding agents and long-context automation",
              "family": "mimo-flash",
              "id": "mimo-v2.6-flash",
              "interleaved": {
                "field": "reasoning_content"
              },
              "last_updated": "2026-09-22",
              "limit": {
                "context": 1048576,
                "output": 131072
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "audio",
                  "video"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "MiMo-V2.6-Flash",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [],
              "release_date": "2026-09-22",
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "mimo-v2.6-flash"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "mimo-v2.6-flash",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "xiaomi/mimo-v2.6-pro",
              "cost": {
                "cache_read": 0.003625,
                "input": 0.435,
                "output": 0.87
              },
              "description": "Stronger MiMo Pro tier for multimodal reasoning and coding-agent execution",
              "family": "mimo-pro",
              "id": "mimo-v2.6-pro",
              "interleaved": {
                "field": "reasoning_content"
              },
              "last_updated": "2026-09-22",
              "limit": {
                "context": 1048576,
                "output": 131072
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "audio",
                  "video"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "MiMo-V2.6-Pro",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [],
              "release_date": "2026-09-22",
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "mimo-v2.6-pro"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "mimo-v2.6-pro",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "minimax/MiniMax-M3",
              "cost": {
                "cache_read": 0.06,
                "context_over_200k": {
                  "cache_read": 0.12,
                  "input": 0.6,
                  "output": 2.4
                },
                "input": 0.3,
                "output": 1.2,
                "tiers": [
                  {
                    "cache_read": 0.12,
                    "input": 0.6,
                    "output": 2.4,
                    "tier": {
                      "size": 512000,
                      "type": "context"
                    }
                  }
                ]
              },
              "description": "MiniMax multimodal coding model for long-context reasoning and agent tasks",
              "family": "minimax-m",
              "id": "minimax-m3",
              "knowledge": "2025-01",
              "last_updated": "2026-06-01",
              "limit": {
                "context": 1000000,
                "output": 131072
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "video"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "MiniMax-M3",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/anthropic/v1",
                "npm": "@ai-sdk/anthropic"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "toggle"
                }
              ],
              "release_date": "2026-06-01",
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "minimax-m3"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "anthropic-messages"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/anthropic"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "minimax-m3",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "minimax/MiniMax-M3.1-Flash",
              "cost": {
                "cache_read": 0.015,
                "input": 0.15,
                "output": 0.6
              },
              "description": "Frontier multimodal coding model with 1M context window and tunable thinking depth",
              "family": "minimax-m-flash",
              "id": "minimax-m3.1-flash",
              "interleaved": {
                "field": "reasoning_content"
              },
              "last_updated": "2026-10-19",
              "limit": {
                "context": 1000000,
                "output": 512000
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "video"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "MiniMax M3.1 Flash",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "low",
                    "medium",
                    "high",
                    "xhigh",
                    "max"
                  ]
                }
              ],
              "release_date": "2026-10-19",
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "minimax-m3.1-flash"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "minimax-m3.1-flash",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "meta/muse-spark-1.2",
              "cost": {
                "cache_read": 0.002,
                "input": 0.1,
                "output": 0.2
              },
              "description": "Muse Spark 1.2 is a coding-focused update to Muse Spark 1.1 with improvements in code generation, complex debugging, codebase understanding, and end-to-end developer workflows.",
              "family": "muse-spark",
              "id": "muse-spark-1.2-contributor",
              "last_updated": "2026-08-05",
              "limit": {
                "context": 1048576,
                "output": 131072
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "video",
                  "pdf",
                  "audio"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Muse Spark 1.2 Contributor",
              "open_weights": false,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1",
                "npm": "@ai-sdk/openai"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "minimal",
                    "low",
                    "medium",
                    "high",
                    "xhigh"
                  ]
                }
              ],
              "release_date": "2026-08-05",
              "structured_output": true,
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "muse-spark-1.2-contributor"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-responses"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "muse-spark-1.2-contributor",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "meta/muse-spark-1.3",
              "cost": {
                "cache_read": 0.002,
                "input": 0.1,
                "output": 0.2
              },
              "description": "Muse Spark 1.3 is a multimodal reasoning model from Meta for coding and agentic workflows.",
              "family": "muse-spark",
              "id": "muse-spark-1.3-contributor",
              "last_updated": "2026-09-02",
              "limit": {
                "context": 1048576,
                "output": 131072
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "video",
                  "pdf",
                  "audio"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Muse Spark 1.3 Contributor",
              "open_weights": false,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1",
                "npm": "@ai-sdk/openai"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "minimal",
                    "low",
                    "medium",
                    "high",
                    "xhigh"
                  ]
                }
              ],
              "release_date": "2026-09-02",
              "structured_output": true,
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "muse-spark-1.3-contributor"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-responses"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "muse-spark-1.3-contributor",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "alibaba/qwen3.7-plus",
              "cost": {
                "cache_read": 0.04,
                "cache_write": 0.5,
                "context_over_200k": {
                  "cache_read": 0.12,
                  "cache_write": 1.5,
                  "input": 1.2,
                  "output": 4.8
                },
                "input": 0.4,
                "output": 1.6,
                "tiers": [
                  {
                    "cache_read": 0.12,
                    "cache_write": 1.5,
                    "input": 1.2,
                    "output": 4.8,
                    "tier": {
                      "size": 256000,
                      "type": "context"
                    }
                  }
                ]
              },
              "description": "Multimodal reasoning model for visual analysis, planning, and tool use",
              "family": "qwen-plus",
              "id": "qwen3.7-plus",
              "knowledge": "2025-04",
              "last_updated": "2026-06-02",
              "limit": {
                "context": 1000000,
                "output": 65536
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "video"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Qwen3.7 Plus",
              "open_weights": false,
              "provider": {
                "api": "https://opencode.ai/inference/go/anthropic/v1",
                "npm": "@ai-sdk/anthropic"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "toggle"
                },
                {
                  "max": 262144,
                  "type": "budget_tokens"
                }
              ],
              "release_date": "2026-06-02",
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "qwen3.7-plus"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "anthropic-messages"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/anthropic"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "qwen3.7-plus",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "alibaba/qwen3.8-flash",
              "cost": {
                "cache_read": 0.016,
                "cache_write": 0.2,
                "input": 0.15,
                "output": 0.47
              },
              "description": "Qwen vision-language model for visual reasoning, documents, and agent tasks",
              "family": "qwen-flash",
              "id": "qwen3.8-flash",
              "last_updated": "2026-08-26",
              "limit": {
                "context": 1000000,
                "output": 131072
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "video"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Qwen3.8 Flash",
              "open_weights": false,
              "provider": {
                "api": "https://opencode.ai/inference/go/anthropic/v1",
                "npm": "@ai-sdk/anthropic"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "toggle"
                },
                {
                  "type": "effort",
                  "values": [
                    "low",
                    "medium",
                    "xhigh"
                  ]
                },
                {
                  "type": "budget_tokens"
                }
              ],
              "release_date": "2026-08-26",
              "structured_output": true,
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "qwen3.8-flash"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "anthropic-messages"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/anthropic"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "qwen3.8-flash",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "alibaba/qwen3.8-max",
              "cost": {
                "cache_read": 0.25,
                "cache_write": 2.5,
                "input": 2,
                "output": 6
              },
              "description": "2.4-trillion-parameter multimodal flagship for coding, professional work, and long-horizon agentic workflows",
              "family": "qwen-max",
              "id": "qwen3.8-max",
              "last_updated": "2026-08-03",
              "limit": {
                "context": 1000000,
                "output": 131072
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "video"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Qwen3.8 Max",
              "open_weights": false,
              "provider": {
                "api": "https://opencode.ai/inference/go/anthropic/v1",
                "npm": "@ai-sdk/anthropic"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "toggle"
                },
                {
                  "type": "effort",
                  "values": [
                    "low",
                    "medium",
                    "xhigh"
                  ]
                },
                {
                  "max": 262144,
                  "type": "budget_tokens"
                }
              ],
              "release_date": "2026-08-03",
              "structured_output": true,
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "qwen3.8-max"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "anthropic-messages"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/anthropic"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "qwen3.8-max",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "alibaba/qwen4-max",
              "cost": {
                "cache_read": 0.075,
                "cache_write": 1.875,
                "input": 1.5,
                "output": 4.5
              },
              "description": "Flagship multimodal model for coding, office productivity, frontend design, and complex agentic tasks",
              "family": "qwen-max",
              "id": "qwen4-max",
              "last_updated": "2026-11-16",
              "limit": {
                "context": 1000000,
                "output": 262144
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "video"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Qwen4 Max",
              "open_weights": false,
              "provider": {
                "api": "https://opencode.ai/inference/go/anthropic/v1",
                "npm": "@ai-sdk/anthropic"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "toggle"
                },
                {
                  "type": "effort",
                  "values": [
                    "low",
                    "high",
                    "xhigh"
                  ]
                },
                {
                  "max": 262144,
                  "type": "budget_tokens"
                }
              ],
              "release_date": "2026-11-16",
              "structured_output": true,
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "qwen4-max"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "anthropic-messages"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/anthropic"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "qwen4-max",
        "reason": null,
        "tool_support": null
      },
      {
        "evidence": {
          "entry": {
            "present": true,
            "value": {
              "attachment": true,
              "canonical_model_id": "stepfun/step-5-preview",
              "cost": {
                "cache_read": 0.1,
                "input": 1,
                "output": 2.7
              },
              "description": "StepFun's next-generation flagship base model for coding and professional knowledge work, with native text, image, and video input and a 1M-token context window",
              "family": "step",
              "id": "step-5-preview",
              "interleaved": {
                "field": "reasoning_content"
              },
              "last_updated": "2026-09-20",
              "limit": {
                "context": 1000000,
                "input": 1000000,
                "output": 65536
              },
              "modalities": {
                "input": [
                  "text",
                  "image",
                  "video"
                ],
                "output": [
                  "text"
                ]
              },
              "name": "Step 5 Preview",
              "open_weights": true,
              "provider": {
                "api": "https://opencode.ai/inference/go/openai/v1"
              },
              "reasoning": true,
              "reasoning_options": [
                {
                  "type": "effort",
                  "values": [
                    "low",
                    "medium",
                    "high"
                  ]
                }
              ],
              "release_date": "2026-09-16",
              "structured_output": true,
              "temperature": true,
              "tool_call": true
            }
          },
          "id": {
            "present": true,
            "value": "step-5-preview"
          },
          "pi": {
            "api": {
              "present": true,
              "value": "openai-completions"
            },
            "baseUrl": {
              "present": true,
              "value": "https://opencode.ai/inference/go/openai/v1"
            },
            "input": {
              "present": true,
              "value": [
                "text",
                "image"
              ]
            },
            "provider": {
              "present": true,
              "value": "opencode-go"
            },
            "type": {
              "present": true,
              "value": "chat"
            }
          },
          "status": {
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "step-5-preview",
        "reason": null,
        "tool_support": null
      }
    ],
    "pi_version": "1.5.0",
    "selection_outcome": "selected",
    "sources": {
      "models_dev": {
        "outcome": "ok",
        "retrieved_at": "2026-11-23T14:50:56.735Z",
        "sha256": "cb002bf463608c324a067db9702469f1d41f800423b250cef34cacdf44354ee4",
        "status": 200,
        "url": "https://models.dev/api.json"
      },
      "pi": {
        "outcome": "ok",
        "retrieved_at": "2026-11-23T14:50:56.548Z",
        "sha256": "4f2343444e7a0ef953589220d6627abdeedca8a3ccf2fd68aa31502e2fb8a2e2",
        "status": 200,
        "url": "https://pi.dev/api/models/providers/opencode-go?types=chat%2Cimage%2Cclassifier"
      }
    }
  },
  "change": "detached-job-launcher",
  "class": "feature",
  "correction_calls": 0,
  "digest": "2c36f3807b1fec28a7a6dd9b9cdd381153912a74c5f2adba5f9ab83209163e18",
  "free_count": 1,
  "free_selected": [
    "hy4-flash-free"
  ],
  "given_neighbours": [],
  "head": "3a330a622be08168cb05930bbdbb8f226590b209",
  "invocation_ceiling": 78,
  "judge_packet": null,
  "preparation": {
    "audit": [
      "prepare-explore · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1184 files, 5472 commits, 12 rules.",
      "opencode-go/deepseek-v4.1-flash: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type",
      "prepare-explore · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1184 files, 5472 commits, 12 rules.",
      "opencode-go/glm-5.3-flash: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type",
      "prepare-explore · endpoint claude-code-plan · model claude-haiku-5-5 · leak check clean over 1184 files, 5472 commits, 12 rules.",
      "prepare-explore · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1184 files, 5472 commits, 12 rules.",
      "opencode-go/mimo-v2.5: dropped catalog field(s) compat, inputLimits, type",
      "prepare-explore · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1184 files, 5472 commits, 12 rules.",
      "opencode-go/mimo-v2.6-flash: dropped catalog field(s) compat, inputLimits, type",
      "prepare-explore · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1184 files, 5472 commits, 12 rules.",
      "opencode-go/qwen3.8-flash: dropped catalog field(s) compat, inputLimits, type",
      "prepare-explore · endpoint opencode-go · model hy4-flash-free · leak check clean over 1184 files, 5472 commits, 12 rules.",
      "opencode-go/hy4-flash-free: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type"
    ],
    "checked_at": "2026-11-23T14:52:33+00:00",
    "models": {
      "claude-code-plan/claude-haiku-5-5": {
        "reason": "claude call failed: exit 1",
        "state": "unreachable"
      },
      "opencode-go/claude-haiku-5-5": {
        "reason": "the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 \"thinking.type.enabled is not supported for this model; use thinking.type.adaptive\" (a Pi adapter setting, bead coding-harness-36za evidence)",
        "state": "skipped"
      },
      "opencode-go/deepseek-v4-pro": {
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/deepseek-v4.1-flash": {
        "reason": "reachable",
        "state": "selected"
      },
      "opencode-go/gemini-4-argon": {
        "reason": "the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint; its measurement is bead coding-harness-twdu); the live catalog of 2026-11-08 lists gemini-4-argon again",
        "state": "skipped"
      },
      "opencode-go/glm-5.2": {
        "reason": "baseline-only; raw {\"api\": {\"present\": false}, \"baseUrl\": {\"present\": false}, \"input\": {\"present\": false}, \"provider\": {\"present\": false}, \"type\": {\"present\": false}}",
        "state": "skipped"
      },
      "opencode-go/glm-5.3": {
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/glm-5.3-flash": {
        "reason": "reachable",
        "state": "selected"
      },
      "opencode-go/gpt-5.6-luna": {
        "reason": "the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 \"Model access is disabled\"",
        "state": "skipped"
      },
      "opencode-go/gpt-6-luna": {
        "reason": "the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 \"Model access is disabled\"",
        "state": "skipped"
      },
      "opencode-go/grok-4.7": {
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/hy3": {
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/hy4": {
        "reason": "the model hy4 has no dated reading of its data terms (gelesen is not an ISO date YYYY-MM-DD)",
        "state": "skipped"
      },
      "opencode-go/hy4-preview": {
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/kimi-k2.7-code": {
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/kimi-k3": {
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/kimi-k3.1-pro": {
        "reason": "the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)",
        "state": "skipped"
      },
      "opencode-go/longcat-2.0": {
        "reason": "deprecated: not in the substitute pool",
        "state": "not-probed"
      },
      "opencode-go/mimo-v2.5": {
        "reason": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5 has been deprecated.\"}",
        "state": "unreachable"
      },
      "opencode-go/mimo-v2.5-pro": {
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/mimo-v2.6-flash": {
        "reason": "reachable",
        "state": "selected"
      },
      "opencode-go/mimo-v2.6-pro": {
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/minimax-m3": {
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/minimax-m3.1-flash": {
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/muse-spark-1.2-contributor": {
        "reason": "the model muse-spark-1.2-contributor has no dated reading of its data terms (gelesen is not an ISO date YYYY-MM-DD)",
        "state": "skipped"
      },
      "opencode-go/muse-spark-1.3-contributor": {
        "reason": "the model muse-spark-1.3-contributor has no dated reading of its data terms (gelesen is not an ISO date YYYY-MM-DD)",
        "state": "skipped"
      },
      "opencode-go/qwen3.7-plus": {
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/qwen3.8-flash": {
        "reason": "reachable",
        "state": "selected"
      },
      "opencode-go/qwen3.8-max": {
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/qwen4-max": {
        "reason": "the model qwen4-max has no dated reading of its data terms (gelesen is not an ISO date YYYY-MM-DD)",
        "state": "skipped"
      },
      "opencode-go/step-5-preview": {
        "reason": "",
        "state": "not-probed"
      }
    },
    "pool": [
      {
        "anfragen_5h": 43330.0,
        "model": "deepseek-v4.1-flash"
      },
      {
        "anfragen_5h": 30100.0,
        "model": "mimo-v2.5"
      },
      {
        "anfragen_5h": 30100.0,
        "model": "mimo-v2.6-flash"
      },
      {
        "anfragen_5h": 6320.0,
        "model": "glm-5.3-flash"
      },
      {
        "anfragen_5h": 5400.0,
        "model": "qwen3.8-flash"
      },
      {
        "anfragen_5h": 4300.0,
        "model": "hy3"
      },
      {
        "anfragen_5h": 4300.0,
        "model": "qwen3.7-plus"
      },
      {
        "anfragen_5h": 3880.0,
        "model": "minimax-m3.1-flash"
      },
      {
        "anfragen_5h": 3250.0,
        "model": "mimo-v2.5-pro"
      },
      {
        "anfragen_5h": 3250.0,
        "model": "mimo-v2.6-pro"
      },
      {
        "anfragen_5h": 3200.0,
        "model": "minimax-m3"
      },
      {
        "anfragen_5h": 1350.0,
        "model": "hy4-preview"
      },
      {
        "anfragen_5h": 1350.0,
        "model": "kimi-k2.7-code"
      },
      {
        "anfragen_5h": 1050.0,
        "model": "deepseek-v4-pro"
      },
      {
        "anfragen_5h": 430.0,
        "model": "step-5-preview"
      },
      {
        "anfragen_5h": 220.0,
        "model": "glm-5.3"
      },
      {
        "anfragen_5h": 169.0,
        "model": "grok-4.7"
      },
      {
        "anfragen_5h": 160.0,
        "model": "qwen3.8-max"
      },
      {
        "anfragen_5h": 110.0,
        "model": "kimi-k3"
      }
    ],
    "unfilled": {
      "online": [],
      "repository": []
    },
    "unread": [
      "hy4",
      "muse-spark-1.2-contributor",
      "muse-spark-1.3-contributor",
      "qwen4-max"
    ]
  },
  "receipt_id": "a074d69181c6e89d450b1256ded8e76880f164d369229e41f6c8a55091414e3c",
  "resume": {
    "interrupted": [],
    "not_reused": [
      [
        "finders-0-3",
        "endpoint"
      ],
      [
        "merge",
        "prompt"
      ]
    ],
    "reasons": [],
    "source_run": "ff73486d6d990feb0c2424c0f347e2e2",
    "usable": true
  },
  "run_id": "78d86db692f0b3f8ac643375833febff",
  "schema": "research-swarm/v2",
  "selection": {
    "online": [
      {
        "endpoint": "opencode-go",
        "mark": "maintainer's choice",
        "model": "deepseek-v4.1-flash",
        "seat": 1
      },
      {
        "endpoint": "opencode-go",
        "mark": "maintainer's choice",
        "model": "glm-5.3-flash",
        "seat": 2
      },
      {
        "endpoint": "opencode-go",
        "mark": "maintainer's choice",
        "model": "qwen3.8-flash",
        "seat": 3
      }
    ],
    "repository": [
      {
        "endpoint": "opencode-go",
        "mark": "maintainer's choice",
        "model": "deepseek-v4.1-flash",
        "seat": 1
      },
      {
        "endpoint": "opencode-go",
        "mark": "maintainer's choice",
        "model": "glm-5.3-flash",
        "seat": 2
      },
      {
        "endpoint": "opencode-go",
        "mark": "substitute for 3",
        "model": "mimo-v2.6-flash",
        "seat": 3
      }
    ]
  },
  "slots": [
    {
      "attempt": 1,
      "corrects": null,
      "ended_at": "2026-11-23T14:34:19Z",
      "endpoint": "opencode-go",
      "error": null,
      "final_attempt": null,
      "launched": false,
      "launched_in": "ff73486d6d990feb0c2424c0f347e2e2",
      "leak_check": {
        "clean": true,
        "commits": 5471,
        "files": 1184,
        "rules": 12
      },
      "model": "deepseek-v4.1-flash",
      "outcome": "ok",
      "prompt_sha256": "9585ed2f8dc0b781f64769cdcf7d4ef9c1a9addff09411578f019bb1e4e2142a",
      "required": true,
      "reused_from": "ff73486d6d990feb0c2424c0f347e2e2",
      "seat": 1,
      "slot_id": "finders-0-1",
      "stage": "finders",
      "started_at": "2026-11-23T14:25:58Z",
      "topic": null
    },
    {
      "attempt": 1,
      "corrects": null,
      "ended_at": "2026-11-23T14:27:42Z",
      "endpoint": "opencode-go",
      "error": null,
      "final_attempt": null,
      "launched": false,
      "launched_in": "ff73486d6d990feb0c2424c0f347e2e2",
      "leak_check": {
        "clean": true,
        "commits": 5471,
        "files": 1184,
        "rules": 12
      },
      "model": "glm-5.3-flash",
      "outcome": "ok",
      "prompt_sha256": "9585ed2f8dc0b781f64769cdcf7d4ef9c1a9addff09411578f019bb1e4e2142a",
      "required": true,
      "reused_from": "ff73486d6d990feb0c2424c0f347e2e2",
      "seat": 2,
      "slot_id": "finders-0-2",
      "stage": "finders",
      "started_at": "2026-11-23T14:26:10Z",
      "topic": null
    },
    {
      "attempt": 1,
      "corrects": null,
      "ended_at": "2026-11-23T15:21:39Z",
      "endpoint": "opencode-go",
      "error": null,
      "final_attempt": null,
      "launched": true,
      "launched_in": null,
      "leak_check": {
        "clean": true,
        "commits": 5472,
        "files": 1184,
        "rules": 12
      },
      "model": "mimo-v2.6-flash",
      "outcome": "ok",
      "prompt_sha256": "9585ed2f8dc0b781f64769cdcf7d4ef9c1a9addff09411578f019bb1e4e2142a",
      "required": true,
      "reused_from": null,
      "seat": 3,
      "slot_id": "finders-0-3",
      "stage": "finders",
      "started_at": "2026-11-23T14:52:44Z",
      "topic": null
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-opus-5-5",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": null,
      "slot_id": "judge",
      "stage": "judge",
      "started_at": null,
      "topic": null
    },
    {
      "attempt": 1,
      "corrects": null,
      "ended_at": "2026-11-23T15:21:50Z",
      "endpoint": "claude-code-plan",
      "error": null,
      "final_attempt": null,
      "launched": true,
      "launched_in": null,
      "leak_check": {
        "clean": true,
        "commits": 5474,
        "files": 1184,
        "rules": 12
      },
      "model": "claude-opus-5-5",
      "outcome": "failed",
      "prompt_sha256": "240feacb455feaa9ab9105e4cab8da2c6587f82e09a797d8e39c4ee6f463d366",
      "required": true,
      "reused_from": null,
      "seat": null,
      "slot_id": "merge",
      "stage": "merge",
      "started_at": "2026-11-23T15:21:48Z",
      "topic": null
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-opus-5-5",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": null,
      "slot_id": "sentence",
      "stage": "sentence",
      "started_at": null,
      "topic": null
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "deepseek-v4.1-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 1,
      "slot_id": "topics-1-1",
      "stage": "topics",
      "started_at": null,
      "topic": 1
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 2,
      "slot_id": "topics-1-2",
      "stage": "topics",
      "started_at": null,
      "topic": 1
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 3,
      "slot_id": "topics-1-3",
      "stage": "topics",
      "started_at": null,
      "topic": 1
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "deepseek-v4.1-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 1,
      "slot_id": "topics-10-1",
      "stage": "topics",
      "started_at": null,
      "topic": 10
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 2,
      "slot_id": "topics-10-2",
      "stage": "topics",
      "started_at": null,
      "topic": 10
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "qwen3.8-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 3,
      "slot_id": "topics-10-3",
      "stage": "topics",
      "started_at": null,
      "topic": 10
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "hy4-flash-free",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": false,
      "reused_from": null,
      "seat": "free",
      "slot_id": "topics-10-free-hy4-flash-free",
      "stage": "topics",
      "started_at": null,
      "topic": 10
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "deepseek-v4.1-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 1,
      "slot_id": "topics-11-1",
      "stage": "topics",
      "started_at": null,
      "topic": 11
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 2,
      "slot_id": "topics-11-2",
      "stage": "topics",
      "started_at": null,
      "topic": 11
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "qwen3.8-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 3,
      "slot_id": "topics-11-3",
      "stage": "topics",
      "started_at": null,
      "topic": 11
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "hy4-flash-free",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": false,
      "reused_from": null,
      "seat": "free",
      "slot_id": "topics-11-free-hy4-flash-free",
      "stage": "topics",
      "started_at": null,
      "topic": 11
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "deepseek-v4.1-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 1,
      "slot_id": "topics-2-1",
      "stage": "topics",
      "started_at": null,
      "topic": 2
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 2,
      "slot_id": "topics-2-2",
      "stage": "topics",
      "started_at": null,
      "topic": 2
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 3,
      "slot_id": "topics-2-3",
      "stage": "topics",
      "started_at": null,
      "topic": 2
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "deepseek-v4.1-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 1,
      "slot_id": "topics-3-1",
      "stage": "topics",
      "started_at": null,
      "topic": 3
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 2,
      "slot_id": "topics-3-2",
      "stage": "topics",
      "started_at": null,
      "topic": 3
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 3,
      "slot_id": "topics-3-3",
      "stage": "topics",
      "started_at": null,
      "topic": 3
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "deepseek-v4.1-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 1,
      "slot_id": "topics-4-1",
      "stage": "topics",
      "started_at": null,
      "topic": 4
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 2,
      "slot_id": "topics-4-2",
      "stage": "topics",
      "started_at": null,
      "topic": 4
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 3,
      "slot_id": "topics-4-3",
      "stage": "topics",
      "started_at": null,
      "topic": 4
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "deepseek-v4.1-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 1,
      "slot_id": "topics-5-1",
      "stage": "topics",
      "started_at": null,
      "topic": 5
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 2,
      "slot_id": "topics-5-2",
      "stage": "topics",
      "started_at": null,
      "topic": 5
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 3,
      "slot_id": "topics-5-3",
      "stage": "topics",
      "started_at": null,
      "topic": 5
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "deepseek-v4.1-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 1,
      "slot_id": "topics-6-1",
      "stage": "topics",
      "started_at": null,
      "topic": 6
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 2,
      "slot_id": "topics-6-2",
      "stage": "topics",
      "started_at": null,
      "topic": 6
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 3,
      "slot_id": "topics-6-3",
      "stage": "topics",
      "started_at": null,
      "topic": 6
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "deepseek-v4.1-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 1,
      "slot_id": "topics-7-1",
      "stage": "topics",
      "started_at": null,
      "topic": 7
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 2,
      "slot_id": "topics-7-2",
      "stage": "topics",
      "started_at": null,
      "topic": 7
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 3,
      "slot_id": "topics-7-3",
      "stage": "topics",
      "started_at": null,
      "topic": 7
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "deepseek-v4.1-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 1,
      "slot_id": "topics-8-1",
      "stage": "topics",
      "started_at": null,
      "topic": 8
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 2,
      "slot_id": "topics-8-2",
      "stage": "topics",
      "started_at": null,
      "topic": 8
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 3,
      "slot_id": "topics-8-3",
      "stage": "topics",
      "started_at": null,
      "topic": 8
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "deepseek-v4.1-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 1,
      "slot_id": "topics-9-1",
      "stage": "topics",
      "started_at": null,
      "topic": 9
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 2,
      "slot_id": "topics-9-2",
      "stage": "topics",
      "started_at": null,
      "topic": 9
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "qwen3.8-flash",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": true,
      "reused_from": null,
      "seat": 3,
      "slot_id": "topics-9-3",
      "stage": "topics",
      "started_at": null,
      "topic": 9
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "opencode-go",
      "error": "never started: incomplete - the map merge failed: merge (failed); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "hy4-flash-free",
      "outcome": "not-started",
      "prompt_sha256": null,
      "required": false,
      "reused_from": null,
      "seat": "free",
      "slot_id": "topics-9-free-hy4-flash-free",
      "stage": "topics",
      "started_at": null,
      "topic": 9
    }
  ],
  "status": "incomplete - the map merge failed: merge (failed); no later stage starts.",
  "untracked": {}
}
```

```research-swarm/v2 partial
{"error": null, "outcome": "failed", "receipts": "", "slot_id": "merge", "stderr": "", "stdout": "You've hit your 5-hour limit · resets 5pm (Europe/Berlin)\n"}
```

### Audit

- Stage-2 call, 2026-11-23: swarm finder · run 78d86db692f0b3f8ac643375833febff · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1184 files, 5472 commits, 12 rules.
- models.json for mimo-v2.6-flash: opencode-go/mimo-v2.6-flash: dropped catalog field(s) compat, inputLimits, type
- Swarm outcome, 2026-11-23: swarm finder · run 78d86db692f0b3f8ac643375833febff · model mimo-v2.6-flash · ok.
- Stage-2 call, 2026-11-23: swarm finder_merge · run 78d86db692f0b3f8ac643375833febff · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1184 files, 5474 commits, 12 rules.
- Swarm outcome, 2026-11-23: swarm finder_merge · run 78d86db692f0b3f8ac643375833febff · model claude-opus-5-5 · failed.

run 78d86db692f0b3f8ac643375833febff status: incomplete - the map merge failed: merge (failed); no later stage starts..

<!-- /research-swarm/v2 -->
