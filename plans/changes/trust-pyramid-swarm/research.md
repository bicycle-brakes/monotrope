---
title: "Research — trust-pyramid-swarm"
status: draft
implementation_status: none
date: 2026-11-18
last_reviewed: 2026-11-18
updated: 2026-11-19
supersedes: null
superseded_by: null
bead: coding-harness-5kvq
class: feature
neighbours: []
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: [{kind: llm-session, name: stage2-research-swarm, version: "2026-11-18"}, {kind: llm-session, name: stage2-research-swarm, version: "2026-11-19"}]
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# trust pyramid swarm — Research

<!-- research-swarm/v2 run bc0811efa646dec007c9f5993a6648e1 -->

## Research swarm — 2026-11-18

run bc0811efa646dec007c9f5993a6648e1 · class feature · baseline HEAD 246324996995 · input digest 2b9396dd85e092f6

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
              "family": "beam",
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
              "family": "Hy",
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
              "family": "longcat",
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
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "longcat-2.5-free",
        "reason": "excluded"
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
              "family": "deepseek-thinking",
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
        "id": "glm-5.2",
        "reason": null,
        "tool_support": null
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
              "family": "Hy",
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
              "family": "Hy",
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
              "family": "Hy",
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
              "family": "kimi-k2",
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
              "family": "kimi-k3",
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
              "family": "kimi-k3",
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
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "longcat-2.0",
        "reason": null,
        "tool_support": null
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
              "family": "mimo-v2.5",
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
              "family": "mimo-v2.5-pro",
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
              "family": "mimo",
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
              "family": "mimo",
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
              "family": "minimax-m3",
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
              "family": "minimax",
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
              "family": "muse",
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
              "family": "muse",
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
              "family": "qwen3.7-plus",
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
              "family": "qwen",
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
              "family": "qwen3.8-max",
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
              "family": "qwen4-max",
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
        "retrieved_at": "2026-11-18T16:20:24.724Z",
        "sha256": "a8f6096b627647d08a40d0e8a50a00c0238397bed622cc3e70b2ecaba072c6b5",
        "status": 200,
        "url": "https://models.dev/api.json"
      },
      "pi": {
        "outcome": "ok",
        "retrieved_at": "2026-11-18T16:20:25.204Z",
        "sha256": "a92bafaf621ca5ae078440b4e2444260e5cfbb92317adec5c9f2ba913a2b621e",
        "status": 200,
        "url": "https://pi.dev/api/models/providers/opencode-go?types=chat%2Cimage%2Cclassifier"
      }
    }
  },
  "change": "trust-pyramid-swarm",
  "class": "feature",
  "correction_calls": 0,
  "digest": "2b9396dd85e092f6cf2f04ba2fbfa3f4cee13907a2d16d7f7a45fdb91f8de676",
  "free_count": 1,
  "free_selected": [
    "hy4-flash-free"
  ],
  "given_neighbours": [],
  "head": "246324996995133d83f92528694527de78f758cc",
  "invocation_ceiling": 78,
  "judge_packet": null,
  "preparation": {
    "audit": [
      "prepare-explore · endpoint claude-code-plan · model claude-haiku-5-5 · leak check clean over 1117 files, 4658 commits, 12 rules.",
      "prepare-explore · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1117 files, 4658 commits, 12 rules.",
      "opencode-go/deepseek-v4.1-flash: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type",
      "prepare-explore · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1117 files, 4658 commits, 12 rules.",
      "opencode-go/mimo-v2.5: dropped catalog field(s) compat, inputLimits, type",
      "prepare-explore · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1117 files, 4658 commits, 12 rules.",
      "opencode-go/mimo-v2.6-flash: dropped catalog field(s) compat, inputLimits, type",
      "prepare-explore · endpoint opencode-go · model longcat-2.0 · leak check clean over 1117 files, 4658 commits, 12 rules.",
      "opencode-go/longcat-2.0: dropped catalog field(s) compat, type",
      "prepare-explore · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1117 files, 4658 commits, 12 rules.",
      "opencode-go/glm-5.3-flash: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type",
      "prepare-explore · endpoint opencode-go · model hy4-flash-free · leak check clean over 1117 files, 4658 commits, 12 rules.",
      "opencode-go/hy4-flash-free: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type"
    ],
    "checked_at": "2026-11-18T16:21:34+00:00",
    "models": {
      "claude-code-plan/claude-haiku-5-5": {
        "reason": "reachable",
        "state": "selected"
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
        "reason": "",
        "state": "not-probed"
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
        "reason": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/go.\"}",
        "state": "unreachable"
      },
      "opencode-go/mimo-v2.5": {
        "reason": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5 has been deprecated. Use mimo-v2.6-flash instead.\"}",
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
        "reason": "",
        "state": "not-probed"
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
        "anfragen_5h": 11400.0,
        "model": "longcat-2.0"
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
        "anfragen_5h": 880.0,
        "model": "glm-5.2"
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
  "receipt_id": "7480e21a4faa153d84388416223f52a1d7f32177a650309309314af207b0e8f3",
  "resume": {
    "interrupted": [],
    "not_reused": [],
    "reasons": [
      "no stored run"
    ],
    "source_run": null,
    "usable": false
  },
  "run_id": "bc0811efa646dec007c9f5993a6648e1",
  "schema": "research-swarm/v2",
  "selection": {
    "online": [
      {
        "endpoint": "opencode-go",
        "mark": "cheapest",
        "model": "deepseek-v4.1-flash",
        "seat": 1
      },
      {
        "endpoint": "opencode-go",
        "mark": "cheapest",
        "model": "mimo-v2.6-flash",
        "seat": 2
      },
      {
        "endpoint": "opencode-go",
        "mark": "cheapest",
        "model": "glm-5.3-flash",
        "seat": 3
      }
    ],
    "repository": [
      {
        "endpoint": "opencode-go",
        "mark": "cheapest",
        "model": "deepseek-v4.1-flash",
        "seat": 1
      },
      {
        "endpoint": "opencode-go",
        "mark": "cheapest",
        "model": "mimo-v2.6-flash",
        "seat": 2
      },
      {
        "endpoint": "claude-code-plan",
        "mark": "preferred",
        "model": "claude-haiku-5-5",
        "seat": 3
      }
    ]
  },
  "slots": [
    {
      "attempt": 1,
      "corrects": null,
      "ended_at": "2026-11-18T16:28:38Z",
      "endpoint": "opencode-go",
      "error": null,
      "final_attempt": null,
      "launched": true,
      "launched_in": null,
      "leak_check": {
        "clean": true,
        "commits": 4658,
        "files": 1117,
        "rules": 12
      },
      "model": "deepseek-v4.1-flash",
      "outcome": "ok",
      "prompt_sha256": "a243cb2e76889965180295ee3848c23a031e0392318d4baa82597d69e599ac4a",
      "required": true,
      "reused_from": null,
      "seat": 1,
      "slot_id": "finders-0-1",
      "stage": "finders",
      "started_at": "2026-11-18T16:21:42Z",
      "topic": null
    },
    {
      "attempt": 1,
      "corrects": null,
      "ended_at": "2026-11-18T16:41:50Z",
      "endpoint": "opencode-go",
      "error": null,
      "final_attempt": null,
      "launched": true,
      "launched_in": null,
      "leak_check": {
        "clean": true,
        "commits": 4658,
        "files": 1117,
        "rules": 12
      },
      "model": "mimo-v2.6-flash",
      "outcome": "timed-out",
      "prompt_sha256": "a243cb2e76889965180295ee3848c23a031e0392318d4baa82597d69e599ac4a",
      "required": true,
      "reused_from": null,
      "seat": 2,
      "slot_id": "finders-0-2",
      "stage": "finders",
      "started_at": "2026-11-18T16:21:50Z",
      "topic": null
    },
    {
      "attempt": 1,
      "corrects": null,
      "ended_at": "2026-11-18T16:23:17Z",
      "endpoint": "claude-code-plan",
      "error": null,
      "final_attempt": null,
      "launched": true,
      "launched_in": null,
      "leak_check": {
        "clean": true,
        "commits": 4658,
        "files": 1117,
        "rules": 12
      },
      "model": "claude-haiku-5-5",
      "outcome": "ok",
      "prompt_sha256": "a243cb2e76889965180295ee3848c23a031e0392318d4baa82597d69e599ac4a",
      "required": true,
      "reused_from": null,
      "seat": 3,
      "slot_id": "finders-0-3",
      "stage": "finders",
      "started_at": "2026-11-18T16:21:58Z",
      "topic": null
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "slot_id": "merge",
      "stage": "merge",
      "started_at": null,
      "topic": null
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
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
      "error": "never started: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
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
  "status": "incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts.",
  "untracked": {
    "plans/changes/trust-pyramid-swarm/research.md": "1cab8869199f6164d5e6a16e4554f687fd55b8c0b0a0ae9995b51a0f522d1348"
  }
}
```

### Audit

- Stage-2 call, 2026-11-18: swarm finder · run bc0811efa646dec007c9f5993a6648e1 · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1117 files, 4658 commits, 12 rules.
- models.json for deepseek-v4.1-flash: opencode-go/deepseek-v4.1-flash: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type
- Stage-2 call, 2026-11-18: swarm finder · run bc0811efa646dec007c9f5993a6648e1 · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1117 files, 4658 commits, 12 rules.
- models.json for mimo-v2.6-flash: opencode-go/mimo-v2.6-flash: dropped catalog field(s) compat, inputLimits, type
- Stage-2 call, 2026-11-18: swarm finder · run bc0811efa646dec007c9f5993a6648e1 · endpoint claude-code-plan · model claude-haiku-5-5 · leak check clean over 1117 files, 4658 commits, 12 rules.
- Swarm outcome, 2026-11-18: swarm finder · run bc0811efa646dec007c9f5993a6648e1 · model claude-haiku-5-5 · ok.
- Swarm outcome, 2026-11-18: swarm finder · run bc0811efa646dec007c9f5993a6648e1 · model deepseek-v4.1-flash · ok.
- Swarm outcome, 2026-11-18: swarm finder · run bc0811efa646dec007c9f5993a6648e1 · model mimo-v2.6-flash · timed-out.

run bc0811efa646dec007c9f5993a6648e1 status: incomplete - a finder failed: finders-0-2 (timed-out); no later stage starts..

<!-- /research-swarm/v2 -->

<!-- research-swarm/v2 run 10522fc13267370c8876b6b93cfbff0c -->

## Research swarm — 2026-11-18

run 10522fc13267370c8876b6b93cfbff0c · class feature · baseline HEAD 246324996995 · input digest a51d7c1916630401

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
              "family": "beam",
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
              "family": "Hy",
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
              "family": "longcat",
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
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "longcat-2.5-free",
        "reason": "excluded"
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
              "family": "deepseek-thinking",
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
        "id": "glm-5.2",
        "reason": null,
        "tool_support": null
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
              "family": "Hy",
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
              "family": "Hy",
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
              "family": "Hy",
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
              "family": "kimi-k2",
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
              "family": "kimi-k3",
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
              "family": "kimi-k3",
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
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "longcat-2.0",
        "reason": null,
        "tool_support": null
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
              "family": "mimo-v2.5",
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
              "family": "mimo-v2.5-pro",
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
              "family": "mimo",
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
              "family": "mimo",
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
              "family": "minimax-m3",
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
              "family": "minimax",
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
              "family": "muse",
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
              "family": "muse",
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
              "family": "qwen3.7-plus",
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
              "family": "qwen",
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
              "family": "qwen3.8-max",
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
              "family": "qwen4-max",
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
        "retrieved_at": "2026-11-18T16:42:36.865Z",
        "sha256": "a8f6096b627647d08a40d0e8a50a00c0238397bed622cc3e70b2ecaba072c6b5",
        "status": 200,
        "url": "https://models.dev/api.json"
      },
      "pi": {
        "outcome": "ok",
        "retrieved_at": "2026-11-18T16:42:36.710Z",
        "sha256": "a92bafaf621ca5ae078440b4e2444260e5cfbb92317adec5c9f2ba913a2b621e",
        "status": 200,
        "url": "https://pi.dev/api/models/providers/opencode-go?types=chat%2Cimage%2Cclassifier"
      }
    }
  },
  "change": "trust-pyramid-swarm",
  "class": "feature",
  "correction_calls": 0,
  "digest": "a51d7c191663040146723ca196a024a94f713b10d4d8d1302ded5856f14865d4",
  "free_count": 1,
  "free_selected": [
    "hy4-flash-free"
  ],
  "given_neighbours": [],
  "head": "246324996995133d83f92528694527de78f758cc",
  "invocation_ceiling": 78,
  "judge_packet": null,
  "preparation": {
    "audit": [
      "prepare-explore · endpoint claude-code-plan · model claude-haiku-5-5 · leak check clean over 1117 files, 4670 commits, 12 rules.",
      "prepare-explore · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1117 files, 4670 commits, 12 rules.",
      "opencode-go/deepseek-v4.1-flash: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type",
      "prepare-explore · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1117 files, 4670 commits, 12 rules.",
      "opencode-go/mimo-v2.5: dropped catalog field(s) compat, inputLimits, type",
      "prepare-explore · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1117 files, 4670 commits, 12 rules.",
      "opencode-go/mimo-v2.6-flash: dropped catalog field(s) compat, inputLimits, type",
      "prepare-explore · endpoint opencode-go · model longcat-2.0 · leak check clean over 1117 files, 4670 commits, 12 rules.",
      "opencode-go/longcat-2.0: dropped catalog field(s) compat, type",
      "prepare-explore · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1117 files, 4670 commits, 12 rules.",
      "opencode-go/glm-5.3-flash: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type",
      "prepare-explore · endpoint opencode-go · model hy4-flash-free · leak check clean over 1117 files, 4670 commits, 12 rules.",
      "opencode-go/hy4-flash-free: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type"
    ],
    "checked_at": "2026-11-18T16:44:17+00:00",
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
        "reason": "",
        "state": "not-probed"
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
        "reason": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/go.\"}",
        "state": "unreachable"
      },
      "opencode-go/mimo-v2.5": {
        "reason": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5 has been deprecated. Use mimo-v2.6-flash instead.\"}",
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
        "reason": "",
        "state": "not-probed"
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
        "anfragen_5h": 11400.0,
        "model": "longcat-2.0"
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
        "anfragen_5h": 880.0,
        "model": "glm-5.2"
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
  "receipt_id": "e4f602842c3df4444e3b316bf4b3dc4f8a4c89f9d8375c8c9a0fbfe58e346709",
  "resume": {
    "interrupted": [],
    "not_reused": [
      [
        "finders-0-1",
        "source run unusable"
      ],
      [
        "finders-0-2",
        "source run unusable"
      ],
      [
        "finders-0-3",
        "source run unusable"
      ]
    ],
    "reasons": [
      "binding changed: research-swarm-limits.yaml"
    ],
    "source_run": "bc0811efa646dec007c9f5993a6648e1",
    "usable": false
  },
  "run_id": "10522fc13267370c8876b6b93cfbff0c",
  "schema": "research-swarm/v2",
  "selection": {
    "online": [
      {
        "endpoint": "opencode-go",
        "mark": "cheapest",
        "model": "deepseek-v4.1-flash",
        "seat": 1
      },
      {
        "endpoint": "opencode-go",
        "mark": "cheapest",
        "model": "mimo-v2.6-flash",
        "seat": 2
      },
      {
        "endpoint": "opencode-go",
        "mark": "cheapest",
        "model": "glm-5.3-flash",
        "seat": 3
      }
    ],
    "repository": [
      {
        "endpoint": "opencode-go",
        "mark": "cheapest",
        "model": "deepseek-v4.1-flash",
        "seat": 1
      },
      {
        "endpoint": "opencode-go",
        "mark": "cheapest",
        "model": "mimo-v2.6-flash",
        "seat": 2
      },
      {
        "endpoint": "opencode-go",
        "mark": "substitute for 3",
        "model": "glm-5.3-flash",
        "seat": 3
      }
    ]
  },
  "slots": [
    {
      "attempt": 1,
      "corrects": null,
      "ended_at": "2026-11-18T16:51:39Z",
      "endpoint": "opencode-go",
      "error": null,
      "final_attempt": null,
      "launched": true,
      "launched_in": null,
      "leak_check": {
        "clean": true,
        "commits": 4670,
        "files": 1117,
        "rules": 12
      },
      "model": "deepseek-v4.1-flash",
      "outcome": "ok",
      "prompt_sha256": "30bb01dd036d2b1abc7625e33a05dc92bcc0d7a0d6398e9c48a1555097673d27",
      "required": true,
      "reused_from": null,
      "seat": 1,
      "slot_id": "finders-0-1",
      "stage": "finders",
      "started_at": "2026-11-18T16:44:28Z",
      "topic": null
    },
    {
      "attempt": 1,
      "corrects": null,
      "ended_at": "2026-11-18T17:17:24Z",
      "endpoint": "opencode-go",
      "error": null,
      "final_attempt": null,
      "launched": true,
      "launched_in": null,
      "leak_check": {
        "clean": true,
        "commits": 4670,
        "files": 1117,
        "rules": 12
      },
      "model": "mimo-v2.6-flash",
      "outcome": "ok",
      "prompt_sha256": "30bb01dd036d2b1abc7625e33a05dc92bcc0d7a0d6398e9c48a1555097673d27",
      "required": true,
      "reused_from": null,
      "seat": 2,
      "slot_id": "finders-0-2",
      "stage": "finders",
      "started_at": "2026-11-18T16:44:38Z",
      "topic": null
    },
    {
      "attempt": 1,
      "corrects": null,
      "ended_at": "2026-11-18T16:46:21Z",
      "endpoint": "opencode-go",
      "error": null,
      "final_attempt": null,
      "launched": true,
      "launched_in": null,
      "leak_check": {
        "clean": true,
        "commits": 4670,
        "files": 1117,
        "rules": 12
      },
      "model": "glm-5.3-flash",
      "outcome": "ok",
      "prompt_sha256": "30bb01dd036d2b1abc7625e33a05dc92bcc0d7a0d6398e9c48a1555097673d27",
      "required": true,
      "reused_from": null,
      "seat": 3,
      "slot_id": "finders-0-3",
      "stage": "finders",
      "started_at": "2026-11-18T16:44:49Z",
      "topic": null
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
      "ended_at": "2026-11-18T17:17:32Z",
      "endpoint": "claude-code-plan",
      "error": null,
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": {
        "clean": false,
        "refused": "the leak check is not clean; the call does not start"
      },
      "model": "claude-opus-5-5",
      "outcome": "refused",
      "prompt_sha256": "129246672d0cc19486aa934c97ce60511560f5169233163d50f5f83ce4aa7af1",
      "required": true,
      "reused_from": null,
      "seat": null,
      "slot_id": "merge",
      "stage": "merge",
      "started_at": null,
      "topic": null
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "mimo-v2.6-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "glm-5.3-flash",
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
      "error": "never started: incomplete - a declaration or leak check refused a call; every queued call was cancelled",
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
  "status": "incomplete - a declaration or leak check refused a call; every queued call was cancelled",
  "untracked": {
    "plans/changes/trust-pyramid-swarm/research.md": "77773fc340644d8e010e332dbe19c5e02addd7e59f375a7f0e6b7b084ce11a9a"
  }
}
```

### Audit

- Stage-2 call, 2026-11-18: swarm finder · run 10522fc13267370c8876b6b93cfbff0c · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1117 files, 4670 commits, 12 rules.
- models.json for deepseek-v4.1-flash: opencode-go/deepseek-v4.1-flash: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type
- Stage-2 call, 2026-11-18: swarm finder · run 10522fc13267370c8876b6b93cfbff0c · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1117 files, 4670 commits, 12 rules.
- models.json for mimo-v2.6-flash: opencode-go/mimo-v2.6-flash: dropped catalog field(s) compat, inputLimits, type
- Stage-2 call, 2026-11-18: swarm finder · run 10522fc13267370c8876b6b93cfbff0c · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1117 files, 4670 commits, 12 rules.
- models.json for glm-5.3-flash: opencode-go/glm-5.3-flash: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type
- Swarm outcome, 2026-11-18: swarm finder · run 10522fc13267370c8876b6b93cfbff0c · model glm-5.3-flash · ok.
- Swarm outcome, 2026-11-18: swarm finder · run 10522fc13267370c8876b6b93cfbff0c · model deepseek-v4.1-flash · ok.
- Swarm outcome, 2026-11-18: swarm finder · run 10522fc13267370c8876b6b93cfbff0c · model mimo-v2.6-flash · ok.
- Stage-2 call, 2026-11-18: swarm finder_merge · run 10522fc13267370c8876b6b93cfbff0c · endpoint claude-code-plan · model claude-opus-5-5 · refused - the leak check is not clean; the call does not start.

run 10522fc13267370c8876b6b93cfbff0c status: incomplete - a declaration or leak check refused a call; every queued call was cancelled.

<!-- /research-swarm/v2 -->

<!-- research-swarm/v2 run 2277a0edf96e707e63c729ef41b6b50e -->

## Research swarm — 2026-11-19

run 2277a0edf96e707e63c729ef41b6b50e · class feature · baseline HEAD a346441b888f · input digest ec937ad908672f8e

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
              "family": "beam",
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
              "family": "Hy",
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
              "family": "longcat",
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
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "longcat-2.5-free",
        "reason": "excluded"
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
              "family": "deepseek-thinking",
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
              "family": "Hy",
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
              "family": "Hy",
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
              "family": "Hy",
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
              "family": "kimi-k2",
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
              "family": "kimi-k3",
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
              "family": "kimi-k3",
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
            "present": false
          },
          "tool_call": {
            "present": true,
            "value": true
          }
        },
        "id": "longcat-2.0",
        "reason": null,
        "tool_support": null
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
              "family": "mimo-v2.5",
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
              "family": "mimo-v2.5-pro",
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
              "family": "mimo",
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
              "family": "mimo",
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
              "family": "minimax-m3",
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
              "family": "minimax",
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
              "family": "muse",
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
              "family": "muse",
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
              "family": "qwen3.7-plus",
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
              "family": "qwen",
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
              "family": "qwen3.8-max",
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
              "family": "qwen4-max",
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
        "retrieved_at": "2026-11-19T09:23:59.064Z",
        "sha256": "5d31ffdd3ba99204b2dcf433a9b802dc9d0778c0bcd9eb6405ccabc282a2f61e",
        "status": 200,
        "url": "https://models.dev/api.json"
      },
      "pi": {
        "outcome": "ok",
        "retrieved_at": "2026-11-19T09:23:58.905Z",
        "sha256": "4f2343444e7a0ef953589220d6627abdeedca8a3ccf2fd68aa31502e2fb8a2e2",
        "status": 200,
        "url": "https://pi.dev/api/models/providers/opencode-go?types=chat%2Cimage%2Cclassifier"
      }
    }
  },
  "change": "trust-pyramid-swarm",
  "class": "feature",
  "correction_calls": 0,
  "digest": "ec937ad908672f8e27914f23de4889cc94a4c4d18a1625ccb863ac5d27eee772",
  "free_count": 1,
  "free_selected": [
    "hy4-flash-free"
  ],
  "given_neighbours": [],
  "head": "a346441b888fd60fcdd7d00cdaf41406f59f56cd",
  "invocation_ceiling": 78,
  "judge_packet": null,
  "preparation": {
    "audit": [
      "prepare-explore · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1114 files, 4742 commits, 12 rules.",
      "opencode-go/deepseek-v4.1-flash: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type",
      "prepare-explore · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1114 files, 4742 commits, 12 rules.",
      "opencode-go/glm-5.3-flash: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type",
      "prepare-explore · endpoint claude-code-plan · model claude-haiku-5-5 · leak check clean over 1114 files, 4742 commits, 12 rules.",
      "prepare-explore · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1114 files, 4742 commits, 12 rules.",
      "opencode-go/qwen3.8-flash: dropped catalog field(s) compat, inputLimits, type",
      "prepare-explore · endpoint opencode-go · model hy4-flash-free · leak check clean over 1114 files, 4743 commits, 12 rules.",
      "opencode-go/hy4-flash-free: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type"
    ],
    "checked_at": "2026-11-19T09:24:50+00:00",
    "models": {
      "claude-code-plan/claude-haiku-5-5": {
        "reason": "reachable",
        "state": "selected"
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
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/mimo-v2.5": {
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/mimo-v2.5-pro": {
        "reason": "",
        "state": "not-probed"
      },
      "opencode-go/mimo-v2.6-flash": {
        "reason": "",
        "state": "not-probed"
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
        "anfragen_5h": 11400.0,
        "model": "longcat-2.0"
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
  "receipt_id": "7615b414cb6e5369836e83841e018d8e162b8be31cd9ee97069c3833e0bad43b",
  "resume": {
    "interrupted": [],
    "not_reused": [],
    "reasons": [
      "no stored run"
    ],
    "source_run": null,
    "usable": false
  },
  "run_id": "2277a0edf96e707e63c729ef41b6b50e",
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
        "endpoint": "claude-code-plan",
        "mark": "preferred",
        "model": "claude-haiku-5-5",
        "seat": 3
      }
    ]
  },
  "slots": [
    {
      "attempt": 1,
      "corrects": null,
      "ended_at": "2026-11-19T09:30:01Z",
      "endpoint": "opencode-go",
      "error": null,
      "final_attempt": null,
      "launched": true,
      "launched_in": null,
      "leak_check": {
        "clean": true,
        "commits": 4743,
        "files": 1114,
        "rules": 12
      },
      "model": "deepseek-v4.1-flash",
      "outcome": "ok",
      "prompt_sha256": "30bb01dd036d2b1abc7625e33a05dc92bcc0d7a0d6398e9c48a1555097673d27",
      "required": true,
      "reused_from": null,
      "seat": 1,
      "slot_id": "finders-0-1",
      "stage": "finders",
      "started_at": "2026-11-19T09:24:59Z",
      "topic": null
    },
    {
      "attempt": 1,
      "corrects": null,
      "ended_at": "2026-11-19T09:26:08Z",
      "endpoint": "opencode-go",
      "error": null,
      "final_attempt": null,
      "launched": true,
      "launched_in": null,
      "leak_check": {
        "clean": true,
        "commits": 4743,
        "files": 1114,
        "rules": 12
      },
      "model": "glm-5.3-flash",
      "outcome": "ok",
      "prompt_sha256": "30bb01dd036d2b1abc7625e33a05dc92bcc0d7a0d6398e9c48a1555097673d27",
      "required": true,
      "reused_from": null,
      "seat": 2,
      "slot_id": "finders-0-2",
      "stage": "finders",
      "started_at": "2026-11-19T09:25:07Z",
      "topic": null
    },
    {
      "attempt": 1,
      "corrects": null,
      "ended_at": "2026-11-19T09:26:12Z",
      "endpoint": "claude-code-plan",
      "error": "the finder answer is not the four-list locator object",
      "final_attempt": null,
      "launched": true,
      "launched_in": null,
      "leak_check": {
        "clean": true,
        "commits": 4743,
        "files": 1114,
        "rules": 12
      },
      "model": "claude-haiku-5-5",
      "outcome": "invalid-report",
      "prompt_sha256": "30bb01dd036d2b1abc7625e33a05dc92bcc0d7a0d6398e9c48a1555097673d27",
      "required": true,
      "reused_from": null,
      "seat": 3,
      "slot_id": "finders-0-3",
      "stage": "finders",
      "started_at": "2026-11-19T09:25:18Z",
      "topic": null
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "slot_id": "merge",
      "stage": "merge",
      "started_at": null,
      "topic": null
    },
    {
      "attempt": null,
      "corrects": null,
      "ended_at": null,
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "endpoint": "claude-code-plan",
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
      "final_attempt": null,
      "launched": false,
      "launched_in": null,
      "leak_check": null,
      "model": "claude-haiku-5-5",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
      "error": "never started: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
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
  "status": "incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts.",
  "untracked": {
    "plans/changes/trust-pyramid-swarm/research.md": "f14dd45e2e9541486ee51fc10e0eb28934df8f45d9e75f20da57f4897dbb847f"
  }
}
```

```research-swarm/v2 partial
{"error": "the finder answer is not the four-list locator object", "outcome": "invalid-report", "receipts": "", "slot_id": "finders-0-3", "stderr": "", "stdout": "{\n  \"code\": [\n    {\"path\": \"scripts/stage2.py\", \"reference\": \"declared_class\", \"reason\": \"Reads the change's `class:` from the research.md and spec.md headers and refuses missing, invalid or disagreeing declarations; the gap the research note calls a self-declared class.\"},\n    {\"path\": \"scripts/stage2.py\", \"reference\": \"CLASSES\", \"reason\": \"The four-class vocabulary (spike, bounded, feature, architectural) that the header check and the interview minimums both rely on.\"},\n    {\"path\": \"scripts/stage2.py\", \"reference\": \"SWARM_CLASSES\", \"reason\": \"Decides which classes route to the research swarm, so a class change alters the review route.\"},\n    {\"path\": \"scripts/stage2.py\", \"reference\": \"explore\", \"reason\": \"Phase 1 entry point that calls declared_class and then routes a feature or architectural change to the swarm.\"},\n    {\"path\": \"scripts/stage2.py\", \"reference\": \"prepare_explore\", \"reason\": \"Phase 1 step one for swarm classes, which prints the availability report the maintainer answers.\"},\n    {\"path\": \"scripts/stage2.py\", \"reference\": \"run_swarm\", \"reason\": \"Runs the research swarm seats for a feature or architectural change.\"},\n    {\"path\": \"scripts/stage2.py\", \"reference\": \"prepare_loop\", \"reason\": \"Static reachability probe run before a fresh review loop; a plausible hook for any new availability or gate check.\"},\n    {\"path\": \"scripts/stage2.py\", \"reference\": \"review_loop\", \"reason\": \"Phase 4b review loop that the research note's proposals on review and verification would touch.\"},\n    {\"path\": \"scripts/stage2_swarm.py\", \"reference\": \"SEAT_KEYS\", \"reason\": \"Seat declaration keys for the swarm; relevant if the swarm's seat or finder structure changes.\"},\n    {\"path\": \"scripts/stage2_research_run.py\", \"reference\": \"TOPIC_NAMES\", \"reason\": \"Fixed list of research topics the six seats cover; the note's blocks are assessed against this topic set.\"},\n    {\"path\": \"scripts/stage2_research_run.py\", \"reference\": \"TOPIC_SCOPES\", \"reason\": \"Scope per research topic, including public-only online topics.\"},\n    {\"path\": \"scripts/stage2_research_run.py\", \"reference\": \"finder_prompt\", \"reason\": \"Builds the finder brief, the input this trust-pyramid finder trio is given.\"},\n    {\"path\": \"scripts/stage2_research_judge.py\", \"reference\": \"TOPIC_OUTCOMES\", \"reason\": \"Closed vocabulary of topic outcomes, which the reconciling judge reads.\"},\n    {\"path\": \"scripts/stage2_research_report.py\", \"reference\": \"validate_research_report\", \"reason\": \"Checks each seat's report, including the class in its assessment.\"},\n    {\"path\": \"scripts/stage2_research_map.py\", \"reference\": \"validate_given_neighbours\", \"reason\": \"Validates the neighbours a research run is given against the spec header.\"},\n    {\"path\": \"scripts/check_interview_minimums.py\", \"reference\": \"MINIMUMS\", \"reason\": \"Interview minimum per class (feature 3, spike 3, bounded 1, architectural 0), keyed by the same class vocabulary.\"},\n    {\"path\": \"scripts/check_research_handoff.py\", \"reason\": \"Gate `research-handoff` checker; holds interview and spec to the research findings and reads the spec's neighbours header.\"},\n    {\"path\": \"scripts/check_criterion_ledger.py\", \"reason\": \"Gate `criterion-ledger` checker; the criterion-to-test ledger the research note names as a verification strength.\"},\n    {\"path\": \"scripts/check_guard_test_environment.py\", \"reason\": \"Gate `guard-test-environment`; the fail-closed planting-switch check the note cites as present.\"},\n    {\"path\": \"scripts/ramp_valves.py\", \"reference\": \"REGEL_VENTILE\", \"reason\": \"The dated valve dictionary (name to missing rule, enforcer test, deadline) that the note's valve-closing proposal changes.\"},\n    {\"path\": \"scripts/ci_gates.py\", \"reason\": \"Reads decisions/gates.yaml and holds the gate list; any non-blocking gate date or reason-schema check would live here.\"},\n    {\"path\": \"scripts/check_docs.py\", \"reason\": \"Hosts the docs checks behind the `docs-links` report gate that the note measures at 199 findings.\"},\n    {\"path\": \"scripts/plans_registry.py\", \"reason\": \"Registry of plan changes, referenced by the note's missing artefact validator and change-class checks.\"},\n    {\"path\": \"scripts/research_census.py\", \"reason\": \"Gate `research-census` checker that reads research headers and publication metadata.\"},\n    {\"path\": \"scripts/research_capture.py\", \"reason\": \"Captures research output into the change folder; relevant to the research.md header and publication fields.\"},\n    {\"path\": \"docs/governance/regelwerk.md\", \"reference\": \"### G — Gates (Maschine)\", \"reason\": \"Rule family holding the machine gates and their levels and valves, which the note's valve and rule-amendment proposals amend.\"},\n    {\"path\": \"docs/WORKFLOW.md\", \"reference\": \"### Which change gets what\", \"reason\": \"Where the class routing per change is described, the place the note says stated routing and the class must agree.\"},\n    {\"path\": \"docs/WORKFLOW.md\", \"reference\": \"### The routing\", \"reason\": \"Model routing text that the note says lives in two places and should be given one home.\"},\n    {\"path\": \"docs/WORKFLOW.md\", \"reference\": \"### Worktrees — one per change\", \"reason\": \"Worktree rules where the note's worktree decay and pruning proposal would apply.\"},\n    {\"path\": \"docs/WORKFLOW.md\", \"reference\": \"### Night runs\", \"reason\": \"Night-run and recurring-job text that the note's worktree-decay and P1 cap proposals touch.\"},\n    {\"path\": \"prompts/02-spec.md\", \"reason\": \"Spec prompt that names the artefact validator for phase 2, which the note reports as absent from the tree.\"},\n    {\"path\": \"prompts/03-plan.md\", \"reason\": \"Plan prompt naming the phase-3 validator and the criterion ledger the plan must carry.\"},\n    {\"path\": \"prompts/02a-spec-review.md\", \"reason\": \"Spec-review prompt for the optional phase 2a, which the note's dimension and ambiguity checks depend on.\"},\n    {\"path\": \"templates/spec.md\", \"reason\": \"Spec header template carrying the class and neighbours fields that the header checks read.\"},\n    {\"path\": \"templates/findings.md\", \"reason\": \"Findings template that the review and verification-artefact proposals would change.\"},\n    {\"path\": \"decisions/gates.yaml\", \"reference\": \"interview-minimums\", \"reason\": \"Gate declaration for the interview minimums, which carry the class-based requirement.\"},\n    {\"path\": \"decisions/gates.yaml\", \"reference\": \"research-handoff\", \"reason\": \"Gate declaration for the research handoff, the gate the research-swarm change would extend.\"},\n    {\"path\": \"decisions/gates.yaml\", \"reference\": \"question-context\", \"reason\": \"Gate declaration whose reason text the note's prose-debt proposal concerns.\"},\n    {\"path\": \"decisions/gates.yaml\", \"reference\": \"docs-links\", \"reason\": \"Non-blocking gate whose reason names a count (35) while the backlog measures 199; the note's dated-gate proposal targets it.\"},\n    {\"path\": \"tests/test_regelwerk.py\", \"reference\": \"test_every_named_ramp_exists_and_no_valve_is_orphaned\", \"reason\": \"Checks that every valve's named enforcer exists and that no valve is orphaned; any valve change must keep it green.\"},\n    {\"path\": \"tests/test_ramp_valves.py\", \"reference\": \"test_the_valve_list_is_not_empty\", \"reason\": \"Guards the valve list against emptiness.\"},\n    {\"path\": \"tests/test_gate_machinery.py\", \"reference\": \"test_the_ramp_valve_gate_goes_red_when_a_valve_is_due\", \"reason\": \"Checks that the ramp-valve gate goes red when a valve is due, the behaviour the dated-valve proposal relies on.\"},\n    {\"path\": \"tests/test_check_interview_minimums.py\", \"reference\": \"test_adr_change_demands_five_regardless_of_class\", \"reason\": \"Covers the class-based minimum rule that the mechanical class check would touch.\"},\n    {\"path\": \"tests/test_stage2_declaration.py\", \"reason\": \"Covers the class declaration rules in the runner (missing, invalid, disagreeing declarations).\"},\n    {\"path\": \"tests/test_stage2.py\", \"reason\": \"Large runner test file, including the 'at most three rounds' memory test the note cites at line 9881.\"},\n    {\"path\": \"tests/test_stage2_swarm.py\", \"reason\": \"Tests for the swarm module that a class or routing change would affect.\"},\n    {\"path\": \"tests/test_research_handoff.py\", \"reference\": \"test_research_handoff_goes_red_when_a_research_answer_is_removed\", \"reason\": \"Covers the research-handoff gate's red case.\"},\n    {\"path\": \"tests/test_check_criterion_ledger.py\", \"reference\": \"test_gates_yaml_declares_criterion_ledger\", \"reason\": \"Checks that the criterion-ledger gate is declared in gates.yaml.\"},\n    {\"path\": \"tests/test_ci.py\", \"reference\": \"test_research_handoff_blocks_local_and_hosted_verification\", \"reason\": \"Checks that the research-handoff gate blocks both local and hosted verification.\"},\n    {\"path\": \"tests/test_kit.py\", \"reference\": \"test_research_handoff_checker_and_tests_travel\", \"reason\": \"Checks that the research-handoff checker and its tests travel with the kit.\"},\n    {\"path\": \"tests/test_explore_provenance.py\", \"reference\": \"test_active_census_is_enabled\", \"reason\": \"Covers the research census that reads research headers.\"},\n    {\"path\": \"tests/test_regelwerk.py\", \"reason\": \"Verifies the rule map and its enforcer edges, which the note names as the strongest existing check.\"},\n    {\"path\": \"tests/test_workflow_entry.py\", \"reason\": \"Entry-point tests over the workflow document, which the note's 'one home' proposal touches.\"},\n    {\"path\": \"plans/changes/trust-pyramid-swarm/research.md\", \"reference\": \"# trust pyramid swarm — Research\", \"reason\": \"The change's own research file (class feature, neighbours empty), which the research swarm run writes into.\"},\n    {\"path\": \"docs/research/2026-11-18-trust-pyramid-against-the-harness.md\", \"reference\": \"## 6 · The consequence, as a proposal\", \"reason\": \"The source note with the eleven building blocks this change would research and act on.\"},\n    {\"path\": \"docs/research/2026-11-18-trust-pyramid-against-the-harness.md\", \"reference\": \"## 3 · The harness against the pyramid\", \"reason\": \"The layer-by-layer measurement of this repository that the change's claims rest on.\"}\n  ],\n  \"rules\": [\n    {\"path\": \"AGENTS.md\", \"reference\": \"The workflow in one screen\", \"reason\": \"The phase table and gates the change's blocks would alter, including the class gate and the research handoff.\"},\n    {\"path\": \"AGENTS.md\", \"reference\": \"House rules\", \"reason\": \"House rules 1 to 9 (English repository, beads only, one entry point, decision PRs) that bound what the change can do.\"},\n    {\"path\": \"AGENTS.md\", \"reference\": \"Tracker quick reference\", \"reason\": \"Tracker commands the change would use to record beads and their notes.\"},\n    {\"path\": \"AGENTS.md\", \"reference\": \"Sessions across checkouts\", \"reason\": \"Worktree rules that the note's worktree-decay proposal would change.\"},\n    {\"path\": \"AGENTS.md\", \"reference\": \"Communication and session continuity\", \"reason\": \"Rules on open questions, P1 cap and night runs that the note's P1 and night-run proposals touch.\"},\n    {\"path\": \"docs/adr/0020-phase-1-research-swarm.md\", \"reference\": \"## Decision\", \"reason\": \"Governs phase 1 class routing and the checked research handoff that the change extends.\"},\n    {\"path\": \"docs/adr/0014-a-change-claims-its-adr-files.md\", \"reference\": \"## Decision\", \"reason\": \"Governs ADR-file claims and the interview gate; the note's class-check proposal refers to ADR claims.\"},\n    {\"path\": \"docs/adr/0021-review-swarms-until-clean.md\", \"reference\": \"## Decision\", \"reason\": \"Governs the review loop that the note's review and verification proposals sit beside.\"},\n    {\"path\": \"docs/adr/0023-guard-proof-for-test-only-repairs.md\", \"reference\": \"## Decision\", \"reason\": \"Governs the guard proof the note cites as a verification strength.\"},\n    {\"path\": \"docs/adr/0018-every-question-carries-its-context.md\", \"reference\": \"## Decision\", \"reason\": \"Governs question context, the rule the note's prose-debt proposal is measured against.\"},\n    {\"path\": \"docs/adr/0013-every-criterion-names-its-proof.md\", \"reference\": \"## Decision\", \"reason\": \"Governs the criterion ledger the note relies on.\"},\n    {\"path\": \"docs/governance/regelwerk.md\", \"reference\": \"### G — Gates (Maschine)\", \"reason\": \"Human-owned rule set (human-decided) whose levels and valves a change alters only through a decision pull request.\"},\n    {\"path\": \"docs/governance/regelwerk.md\", \"reference\": \"## 4 SYNC IMPACT — was eine Änderung dieser Seite auslöst\", \"reason\": \"States what a change to the rule set triggers, including the version bump the note's valve proposal requires.\"},\n    {\"path\": \"docs/governance/regelwerk.md\", \"reference\": \"## 3 Die Leiter\", \"reason\": \"Defines the level ladder (level 4 block, 3 report, 2 person, 1 convention) the note uses to grade the layers.\"}\n  ],\n  \"tests\": [\n    {\"path\": \"tests/test_regelwerk.py\", \"reference\": \"test_every_named_ramp_exists_and_no_valve_is_orphaned\", \"reason\": \"Would break if a valve closes without its enforcer test existing or leaves an orphan.\"},\n    {\"path\": \"tests/test_ramp_valves.py\", \"reference\": \"test_the_valve_list_is_not_empty\", \"reason\": \"Covers the valve list the note's valve-closing proposal edits.\"},\n    {\"path\": \"tests/test_gate_machinery.py\", \"reference\": \"test_the_ramp_valve_check_runs_green_here\", \"reason\": \"Runs the valve check on the live tree; affected by any change to valves or deadlines.\"},\n    {\"path\": \"tests/test_gate_machinery.py\", \"reference\": \"test_the_ramp_valve_gate_goes_red_when_a_valve_is_due\", \"reason\": \"Covers the red case for a due valve, which the dated-valve proposal depends on.\"},\n    {\"path\": \"tests/test_check_interview_minimums.py\", \"reference\": \"test_adr_change_demands_five_regardless_of_class\", \"reason\": \"Would be affected if the class check changes minimums or ADR routing.\"},\n    {\"path\": \"tests/test_stage2_declaration.py\", \"reason\": \"Would be affected by any change to how the class is declared or checked.\"},\n    {\"path\": \"tests/test_research_handoff.py\", \"reference\": \"test_pending_handoff_is_green_only_before_spec\", \"reason\": \"Would be affected by any change to the research-handoff gate's states.\"},\n    {\"path\": \"tests/test_ci.py\", \"reference\": \"test_research_handoff_blocks_local_and_hosted_verification\", \"reason\": \"Would be affected if the research-handoff gate is altered or moved between jobs.\"},\n    {\"path\": \"tests/test_check_criterion_ledger.py\", \"reference\": \"test_the_plan_prompt_requires_the_ledger\", \"reason\": \"Would be affected by changes to the plan prompt that names the ledger.\"},\n    {\"path\": \"tests/test_stage2_research_map.py\", \"reason\": \"Would be affected by changes to the neighbours validation in the research map.\"},\n    {\"path\": \"tests/test_stage2_research_report.py\", \"reason\": \"Would be affected by changes to the research report validation and its class vocabulary.\"},\n    {\"path\": \"tests/test_stage2_research_judge.py\", \"reason\": \"Would be affected by changes to the judge's topic outcomes.\"},\n    {\"path\": \"tests/test_stage2_research_run.py\", \"reason\": \"Would be affected by changes to topic names, scopes or the finder prompt.\"},\n    {\"path\": \"tests/test_stage2_research_dispatch.py\", \"reason\": \"Would be affected by changes to how the swarm seats are dispatched.\"},\n    {\"path\": \"tests/test_stage2_research_availability.py\", \"reason\": \"Would be affected by changes to the availability receipt that gates a fresh run.\"},\n    {\"path\": \"tests/test_ci.py\", \"reference\": \"test_research_handoff_blocks_local_and_hosted_verification\", \"reason\": \"Gate-list test covering the blocking status of the research-handoff gate in local and hosted verification.\"},\n    {\"path\": \"tests/test_kit.py\", \"reference\": \"test_research_handoff_checker_and_tests_travel\", \"reason\": \"Would be affected if the checker or its tests move out of the kit.\"},\n    {\"path\": \"tests/test_explore_provenance.py\", \"reference\": \"test_active_census_is_enabled\", \"reason\": \"Would be affected by changes to the research census that reads research headers.\"},\n    {\"path\": \"tests/test_check_docs.py\", \"reason\": \"Would be affected by any change to the docs checks behind the docs-links report gate.\"},\n    {\"path\": \"tests/test_gate_catalog.py\", \"reason\": \"Would be affected by changes to gate declarations in decisions/gates.yaml, including reason text and enforcement levels.\"},\n    {\"path\": \"tests/test_stage2.py\", \"reason\": \"Would be affected by any change to explore, prepare_explore or review_loop in the runner, and holds the ADR 0011 memory test.\"},\n    {\"path\": \"tests/test_stage2_swarm.py\", \"reason\": \"Would be affected by any change to the swarm routing by class.\"},\n    {\"path\": \"tests/test_entry_points.py\", \"reason\": \"Would be affected by any change to the instruction file or the entry-point rules.\"},\n    {\"path\": \"tests/test_workflow_entry.py\", \"reason\": \"Would be affected by any change to the phase text or route descriptions in the workflow document.\"}\n  ],\n  \"neighbours\": [\n    {\"path\": \"docs/research/2026-10-08-explore-swarm-proposal.md\", \"reason\": \"Earlier proposal for the explore swarm, the direct precursor of the research swarm this change would research against.\"},\n    {\"path\": \"plans/changes/research-currency/research.md\", \"reference\": \"## 1 · What exists today\", \"reason\": \"Another change researching the research swarm's inputs and existing artefacts, a neighbouring research topic.\"},\n    {\"path\": \"plans/changes/research-currency/spec.md\", \"reason\": \"Spec of a neighbouring research change that mentions the same swarm and validator surfaces.\"},\n    {\"path\": \"plans/changes/harness-decide-adr/research.md\", \"reason\": \"Neighbouring change whose research touches the decision and ADR paths the class and gate changes touch.\"},\n    {\"path\": \"plans/changes/stage2-session/design.md\", \"reason\": \"Design of the stage-2 session path that shares the runner the note's changes would touch.\"},\n    {\"path\": \"plans/changes/adr-repair-check/spec.md\", \"reason\": \"Spec of a neighbouring check on ADR repairs, a sibling to the class-check and mechanical validator proposals.\"},\n    {\"path\": \"plans/changes/archive/2026-11-16-verify-tmp-cleanup/plan.md\", \"reason\": \"Archived plan showing the criterion ledger and verify changes that the research note measures as existing.\"},\n    {\"path\": \"docs/adr/0021-review-swarms-until-clean.md\", \"reference\": \"## Restart amendment — the maintainer restarts a completed loop, 2026-10-21\", \"reason\": \"Amendment that governs when a loop restarts, adjacent to the note's review-loop and verification proposals.\"}\n  ]\n}\n"}
```

### Audit

- Stage-2 call, 2026-11-19: swarm finder · run 2277a0edf96e707e63c729ef41b6b50e · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1114 files, 4743 commits, 12 rules.
- models.json for deepseek-v4.1-flash: opencode-go/deepseek-v4.1-flash: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type
- Stage-2 call, 2026-11-19: swarm finder · run 2277a0edf96e707e63c729ef41b6b50e · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1114 files, 4743 commits, 12 rules.
- models.json for glm-5.3-flash: opencode-go/glm-5.3-flash: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type
- Stage-2 call, 2026-11-19: swarm finder · run 2277a0edf96e707e63c729ef41b6b50e · endpoint claude-code-plan · model claude-haiku-5-5 · leak check clean over 1114 files, 4743 commits, 12 rules.
- Swarm outcome, 2026-11-19: swarm finder · run 2277a0edf96e707e63c729ef41b6b50e · model glm-5.3-flash · ok.
- Swarm outcome, 2026-11-19: swarm finder · run 2277a0edf96e707e63c729ef41b6b50e · model claude-haiku-5-5 · ok.
- Swarm outcome, 2026-11-19: swarm finder · run 2277a0edf96e707e63c729ef41b6b50e · model deepseek-v4.1-flash · ok.

run 2277a0edf96e707e63c729ef41b6b50e status: incomplete - a finder failed: finders-0-3 (invalid-report); no later stage starts..

<!-- /research-swarm/v2 -->
